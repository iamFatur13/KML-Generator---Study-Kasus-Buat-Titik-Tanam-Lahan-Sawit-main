import simplekml
from shapely.geometry import Polygon, Point, LineString
import numpy as np

def get_user_input():
    print("--- Generator Waypoint Sawit (Estate Planning Mode) ---")
    try:
        # 1. Input Konfigurasi
        jarak_raw = input("Masukkan jarak tanam (contoh 8x9): ").lower()
        dx_m, dy_m = map(float, jarak_raw.split('x'))
        buffer_m = float(input("Masukkan jarak buffer dari batas lahan (meter): "))
        interval_batas = 10.0 # Jarak antar WP di garis batas (10m)
        
        # 2. Input Titik Batas
        jml = int(input("Berapa banyak titik koordinat utama batas lahan? "))
        if jml < 3:
            print("Minimal diperlukan 3 titik utama.")
            return None
            
        coords = []
        for i in range(jml):
            while True:
                try:
                    raw_input = input(f"Titik Sudut ke-{i+1} (lon, lat): ")
                    ln, lt = map(float, raw_input.split(','))
                    coords.append((ln, lt))
                    break
                except ValueError:
                    print("Format salah! Gunakan: longitude, latitude")
        
        # 3. Pilih Titik Awal Tanam
        print("\nPilih Titik Awal Tanam (P1):")
        for idx, c in enumerate(coords):
            print(f"{idx+1}. Titik Sudut ke-{idx+1} ({c[0]}, {c[1]})")
        
        pilihan = int(input("Pilihan Anda: "))
        start_node = coords[pilihan-1]

        original_coords = list(coords)
        if coords[0] != coords[-1]:
            coords.append(coords[0])
        
        return original_coords, coords, start_node, dx_m, dy_m, buffer_m, interval_batas
    except Exception as e:
        print(f"Input tidak valid: {e}")
        return None

def generate_kml():
    user_data = get_user_input()
    if not user_data: return
    orig_coords, boundary_coords, start_node, dx_m, dy_m, buffer_m, interval_m = user_data

    kml = simplekml.Kml()
    M_TO_DEG = 0.000009 # Konversi kasar derajat ke meter

    # --- STYLING ---
    style_sudut = simplekml.Style()
    style_sudut.iconstyle.icon.href = 'http://maps.google.com/mapfiles/kml/paddle/red-stars.png'
    
    style_ruas = simplekml.Style()
    style_ruas.iconstyle.icon.href = 'http://maps.google.com/mapfiles/kml/shapes/placemark_circle_highlight.png'
    style_ruas.iconstyle.scale = 0.5
    style_ruas.labelstyle.scale = 0 # Sembunyikan label agar tidak penuh

    style_tanam = simplekml.Style()
    style_tanam.iconstyle.icon.href = 'http://maps.google.com/mapfiles/kml/shapes/target.png'
    style_tanam.iconstyle.scale = 0.6

    # --- 1. FOLDER BATAS & RUAS ---
    fol_batas = kml.newfolder(name="Boundary & Ruas")
    
    # Buat Polygon Area
    poly_obj = fol_batas.newpolygon(name="Area Lahan", outerboundaryis=boundary_coords)
    poly_obj.style.polystyle.color = '4000ff00' # Hijau Transparan

    # Iterasi per ruas untuk membuat WP setiap 10m
    for i in range(len(boundary_coords) - 1):
        p1 = boundary_coords[i]
        p2 = boundary_coords[i+1]
        line = LineString([p1, p2])
        
        # Hitung jarak ruas dalam meter
        dist_m = line.length / M_TO_DEG
        num_points = int(dist_m / interval_m)
        
        # Tambahkan titik Sudut Utama
        pnt_sudut = fol_batas.newpoint(name=f"SUDUT-{i+1}", coords=[p1])
        pnt_sudut.style = style_sudut

        # Tambahkan titik-titik di sepanjang ruas
        if num_points > 1:
            for j in range(1, num_points):
                # Interpolasi posisi berdasarkan jarak
                frac = (j * interval_m) / dist_m
                if frac < 1.0:
                    curr_p = line.interpolate(frac, normalized=True)
                    pnt_r = fol_batas.newpoint(name=f"R{i+1}-{j}", coords=[(curr_p.x, curr_p.y)])
                    pnt_r.style = style_ruas

    # --- 2. GENERASI TITIK TANAM ---
    fol_tanam = kml.newfolder(name="Titik Tanam Sawit")
    poly_geom = Polygon(boundary_coords)
    inner_poly = poly_geom.buffer(-(buffer_m * M_TO_DEG))
    
    if not inner_poly.is_empty:
        minx, miny, maxx, maxy = inner_poly.bounds
        dx, dy = dx_m * M_TO_DEG, dy_m * M_TO_DEG
        
        x_range = np.arange(start_node[0] - (np.ceil((start_node[0]-minx)/dx)*dx), maxx + dx, dx)
        y_range = np.arange(start_node[1] - (np.ceil((start_node[1]-miny)/dy)*dy), maxy + dy, dy)

        count = 1
        for i, y in enumerate(y_range):
            offset = (dx / 2) if i % 2 != 0 else 0
            for x in x_range:
                adj_x = x + offset
                if inner_poly.contains(Point(adj_x, y)):
                    pnt = fol_tanam.newpoint(name=f"S-{count}", coords=[(adj_x, y)])
                    pnt.style = style_tanam
                    count += 1

    # Statistik Luas
    area_ha = (poly_geom.area / (M_TO_DEG**2)) / 10000

    # Save
    fname = f"rencana_tanam_{int(dx_m)}x{int(dy_m)}_B{int(buffer_m)}m_Lengkap.kml"
    kml.save(fname)

    print("\n" + "="*40)
    print(f"PROSES SELESAI:")
    print(f"File KML             : {fname}")
    print(f"Estimasi Luas Lahan  : {area_ha:.2f} Hektar")
    print(f"Jarak Tanam          : {dx_m}m x {dy_m}m")
    print(f"Sempadan (Buffer)    : {buffer_m} meter")
    print(f"Jumlah Titik Tanam   : {count-1} Pokok")
    print(f"Folder di KML        : 'Batas Lahan' & 'Titik Tanam'")
    print("="*40)
    print(f"\nSelesai! File '{fname}' siap digunakan.")
    

if __name__ == "__main__":
    generate_kml()
