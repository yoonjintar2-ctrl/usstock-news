"""간밤 뉴스 6건용 3D 삽화(블렌더 Cycles). 실존 인물·회사 로고 없음.
python3 render_news.py <outdir> [name ...]"""
import bpy, math, sys, os
from mathutils import Vector

OUT = sys.argv[1]
ONLY = sys.argv[2:]
C = {'cream': (0.96, 0.93, 0.86), 'navy': (0.06, 0.16, 0.26), 'coral': (0.88, 0.33, 0.25), 'gold': (0.95, 0.68, 0.22),
     'ink': (0.08, 0.08, 0.09), 'white': (0.97, 0.97, 0.95), 'grey': (0.62, 0.6, 0.56), 'steel': (0.7, 0.72, 0.75),
     'teal': (0.18, 0.45, 0.48), 'brown': (0.35, 0.22, 0.14), 'blue': (0.15, 0.39, 0.65)}
MAT = {}


def mat(name, metal=0.0, rough=0.45, emit=0.0):
    k = f'{name}{metal}{rough}{emit}'
    if k in MAT: return MAT[k]
    m = bpy.data.materials.new(k); m.use_nodes = True
    b = m.node_tree.nodes['Principled BSDF']
    col = (*C[name], 1)
    b.inputs['Base Color'].default_value = col
    b.inputs['Metallic'].default_value = metal
    b.inputs['Roughness'].default_value = rough
    if emit:
        b.inputs['Emission Color'].default_value = col; b.inputs['Emission Strength'].default_value = emit
    MAT[k] = m; return m


def put(obj, m, bevel=0.0):
    obj.data.materials.append(m)
    if bevel:
        bv = obj.modifiers.new('b', 'BEVEL'); bv.width = bevel; bv.segments = 4
    bpy.ops.object.shade_smooth() if obj.type == 'MESH' else None
    return obj


def box(loc, size, m, bevel=0.04, rot=(0, 0, 0)):
    bpy.ops.mesh.primitive_cube_add(location=loc, rotation=rot)
    o = bpy.context.object; o.scale = (size[0] / 2, size[1] / 2, size[2] / 2)
    bpy.ops.object.transform_apply(scale=True)
    return put(o, m, bevel)


def cyl(loc, r, d, m, rot=(0, 0, 0), v=48, bevel=0.0):
    bpy.ops.mesh.primitive_cylinder_add(location=loc, radius=r, depth=d, rotation=rot, vertices=v)
    return put(bpy.context.object, m, bevel)


def cone(loc, r1, r2, d, m, rot=(0, 0, 0)):
    bpy.ops.mesh.primitive_cone_add(location=loc, radius1=r1, radius2=r2, depth=d, rotation=rot, vertices=48)
    return put(bpy.context.object, m)


def sphere(loc, r, m):
    bpy.ops.mesh.primitive_uv_sphere_add(location=loc, radius=r, segments=48, ring_count=24)
    return put(bpy.context.object, m)


def arrow(start, end, r, m):
    s, e = Vector(start), Vector(end); d = e - s; L = d.length; head = min(r * 4.5, L * 0.45)
    dirn = d.normalized(); rot = dirn.to_track_quat('Z', 'Y').to_euler()
    shaft_end = e - dirn * head
    cyl((s + shaft_end) / 2, r, (shaft_end - s).length, m, rot=rot, bevel=0.0)
    cone(shaft_end + dirn * head / 2, r * 2.6, 0, head, m, rot=rot)


def base_scene():
    bpy.ops.wm.read_factory_settings(use_empty=True); MAT.clear()
    sc = bpy.context.scene
    sc.render.engine = 'CYCLES'; sc.cycles.device = 'CPU'; sc.cycles.samples = 48; sc.cycles.use_denoising = True
    sc.render.resolution_x, sc.render.resolution_y = 800, 600
    sc.view_settings.view_transform = 'Standard'; sc.view_settings.look = 'None'; sc.view_settings.exposure = -0.35
    w = bpy.data.worlds.new('w'); sc.world = w; w.use_nodes = True
    w.node_tree.nodes['Background'].inputs[0].default_value = (*C['cream'], 1); w.node_tree.nodes['Background'].inputs[1].default_value = 0.35
    # 바닥 + 벽(무한 배경 느낌)
    bpy.ops.mesh.primitive_plane_add(size=40, location=(0, 0, 0)); put(bpy.context.object, mat('cream', rough=0.9))
    bpy.ops.mesh.primitive_plane_add(size=40, location=(0, 6, 0), rotation=(math.radians(90), 0, 0)); put(bpy.context.object, mat('cream', rough=0.9))
    # 조명
    bpy.ops.object.light_add(type='AREA', location=(-4, -5, 7)); l = bpy.context.object; l.data.energy = 900; l.data.size = 6
    l.rotation_euler = (math.radians(45), 0, math.radians(-35))
    bpy.ops.object.light_add(type='AREA', location=(5, -3, 4)); l = bpy.context.object; l.data.energy = 200; l.data.size = 4
    l.rotation_euler = (math.radians(60), 0, math.radians(50))
    bpy.ops.object.camera_add(location=(0, -9.5, 4.6)); cam = bpy.context.object; sc.camera = cam
    cam.data.lens = 50
    return sc, cam


def aim(cam, target=(0, 0, 1.1)):
    d = Vector(target) - cam.location; cam.rotation_euler = d.to_track_quat('-Z', 'Y').to_euler()


def render(name, sc):
    sc.render.filepath = os.path.join(OUT, f'{name}.png'); bpy.ops.render.render(write_still=True)


# ── 장면들 ────────────────────────────────────────────
def nvda():
    sc, cam = base_scene()
    box((0, 0, 0.35), (3.2, 2.4, 0.7), mat('white'), 0.08)            # 받침대
    box((0, 0, 0.82), (2.2, 2.2, 0.22), mat('ink', 0.3, 0.35), 0.05)   # 칩 기판
    box((0, 0, 1.0), (1.3, 1.3, 0.16), mat('steel', 0.9, 0.2), 0.03)   # 다이
    for i in range(9):                                                  # 금 핀
        t = -0.95 + i * 0.2375
        for x, y in ((t, -1.12), (t, 1.12), (-1.12, t), (1.12, t)):
            box((x, y, 0.82), (0.09 if abs(y) > 1 else 0.14, 0.14 if abs(y) > 1 else 0.09, 0.05), mat('gold', 0.9, 0.25), 0.01)
    for i, h in enumerate((0.8, 1.3, 1.9, 2.6, 3.3)):                  # 커지는 매출 막대
        box((-2.6 + i * 0.75 + 1.3, 2.2, h / 2), (0.5, 0.5, h), mat('coral'), 0.05)
    arrow((2.3, -0.6, 3.0), (2.9, -0.9, 0.9), 0.13, mat('navy'))        # 내려가는 주가
    cam.location = (0.4, -10.5, 5.2); aim(cam, (0.3, 0.6, 1.5)); render('nvda', sc)


def fed():
    sc, cam = base_scene()
    box((0, 0, 0.15), (4.4, 2.6, 0.3), mat('white'), 0.03)
    box((0, 0, 0.4), (4.0, 2.3, 0.2), mat('white'), 0.03)
    for i in range(6):
        cyl((-1.6 + i * 0.64, -0.9, 1.5), 0.17, 2.0, mat('white', rough=0.6))
    box((0, 0.1, 1.5), (3.6, 1.6, 2.0), mat('grey', rough=0.8), 0.02)
    box((0, 0, 2.62), (4.1, 2.3, 0.25), mat('white'), 0.03)
    bpy.ops.mesh.primitive_cone_add(vertices=3, radius1=2.35, depth=2.2, location=(0, 0, 3.15), rotation=(math.radians(90), 0, 0))
    o = bpy.context.object; o.scale = (1, 0.45, 1); put(o, mat('white'))
    arrow((2.6, -0.4, 0.5), (3.1, -0.6, 3.9), 0.14, mat('coral'))      # 오르는 금리
    for i, x in enumerate((-3.3, -2.9)):                                 # 서류 더미
        box((x, -1.1, 0.06 + i * 0.12), (1.2, 0.9, 0.1), mat('white', rough=0.9), 0.01)
    cam.location = (0.5, -9.8, 3.9); aim(cam, (0, 0, 1.7)); render('fed', sc)


def ipo():
    sc, cam = base_scene()
    box((0, 0, 0.5), (2.6, 1.6, 1.0), mat('navy'), 0.06)                # 연단
    cyl((0, 0, 1.35), 0.07, 0.7, mat('gold', 0.9, 0.25))                # 종 받침
    bpy.ops.mesh.primitive_uv_sphere_add(location=(0, 0, 2.05), radius=0.75, segments=64, ring_count=32)
    b = bpy.context.object; b.scale = (1, 1, 1.05); put(b, mat('gold', 0.95, 0.18))
    cyl((0, 0, 1.55), 0.95, 0.18, mat('gold', 0.95, 0.18))              # 종 테두리
    sphere((0, 0, 1.38), 0.16, mat('gold', 0.9, 0.3))
    cyl((0.0, 0.0, 2.9), 0.1, 0.3, mat('gold', 0.9, 0.25))
    import random; random.seed(7)
    for i in range(46):                                                  # 색종이
        x, z = random.uniform(-3.4, 3.4), random.uniform(1.0, 4.6)
        if abs(x) < 1.1 and z < 3.2: continue
        box((x, random.uniform(-0.5, 1.5), z), (0.22, 0.04, 0.14), mat(random.choice(['coral', 'gold', 'navy', 'teal'])), 0.0,
            rot=(random.uniform(0, 3), random.uniform(0, 3), random.uniform(0, 3)))
    arrow((2.2, 0.6, 0.4), (2.8, 0.4, 2.6), 0.12, mat('coral'))
    cam.location = (0, -9.0, 3.6); aim(cam, (0, 0, 1.9)); render('ipo', sc)


def health():
    sc, cam = base_scene()
    # 방패(납작한 원기둥 + 아래 뾰족)
    bpy.ops.mesh.primitive_cylinder_add(vertices=6, radius=1.4, depth=0.35, location=(-0.3, 0, 1.75), rotation=(math.radians(90), 0, math.radians(0)))
    o = bpy.context.object; o.scale = (1, 1.25, 1); put(o, mat('white'), 0.06)
    box((-0.3, -0.225, 1.85), (0.32, 0.12, 1.2), mat('teal'), 0.03); box((-0.3, -0.22, 1.85), (1.2, 0.1, 0.32), mat('teal'), 0.03)
    for i, (x, rz) in enumerate(((1.9, 20), (2.6, -35), (2.2, 70))):   # 캡슐
        cyl((x, -0.6 + i * 0.4, 0.25), 0.22, 0.75, mat('coral' if i % 2 else 'white'), rot=(0, math.radians(90), math.radians(rz)), bevel=0.1)
    box((-2.6, 0.2, 0.05), (1.6, 2.0, 0.1), mat('white', rough=0.9), 0.01)                   # 클립보드
    box((-2.6, 0.2, 0.11), (1.3, 1.6, 0.03), mat('grey', rough=0.9), 0.0)
    arrow((1.7, 0.8, 3.6), (2.2, 0.8, 1.3), 0.13, mat('navy'))
    cam.location = (0, -9.2, 4.2); aim(cam, (-0.1, 0, 1.3)); render('health', sc)


def memory():
    sc, cam = base_scene()
    import random; random.seed(3)
    for layer in range(5):                                               # 쌓인 메모리 모듈
        for j in range(4 - layer // 2):
            x = -1.6 + j * 1.05 + layer * 0.25 + random.uniform(-0.08, 0.08)
            z = 0.12 + layer * 0.26
            box((x, random.uniform(-0.2, 0.2), z), (0.95, 2.4, 0.2), mat('teal', rough=0.5), 0.03, rot=(0, 0, math.radians(random.uniform(-8, 8))))
            for k in range(4):
                box((x, -0.9 + k * 0.6, z + 0.13), (0.55, 0.42, 0.07), mat('ink', 0.3, 0.3), 0.01)
            box((x, 1.25, z), (0.9, 0.12, 0.12), mat('gold', 0.9, 0.25), 0.0)
    arrow((2.5, -0.3, 2.7), (2.8, -0.5, 0.5), 0.13, mat('navy'))
    cam.location = (0.4, -8.2, 5.0); aim(cam, (0.2, 0, 0.8)); render('memory', sc)


def gold_oil():
    sc, cam = base_scene()
    def bar(loc, rot=0):
        bpy.ops.mesh.primitive_cube_add(location=loc, rotation=(0, 0, math.radians(rot)))
        o = bpy.context.object; o.scale = (0.75, 0.35, 0.2)
        bpy.ops.object.transform_apply(scale=True)
        bpy.ops.object.mode_set(mode='EDIT'); bpy.ops.mesh.select_all(action='DESELECT'); bpy.ops.object.mode_set(mode='OBJECT')
        for v in o.data.vertices:
            if v.co.z > 0: v.co.x *= 0.8; v.co.y *= 0.7
        put(o, mat('gold', 1.0, 0.2), 0.03)
    for p in ((-1.9, 0, 0.2, 5), (-0.4, 0.1, 0.2, -4), (-1.15, 0.05, 0.6, 2)):
        bar(p[:3], p[3])
    cyl((1.6, 0.3, 1.0), 0.75, 2.0, mat('navy', 0.4, 0.4), bevel=0.04)  # 드럼통
    for z in (0.35, 1.0, 1.65): cyl((1.6, 0.3, z), 0.78, 0.07, mat('navy', 0.5, 0.35))
    sphere((1.6, -0.5, 0.05), 0.22, mat('ink', 0.2, 0.1))              # 기름 방울
    arrow((-2.6, -0.4, 2.9), (-2.4, -0.6, 1.1), 0.12, mat('coral'))
    arrow((2.75, -0.2, 2.9), (2.85, -0.4, 0.9), 0.12, mat('coral'))
    cam.location = (0, -9.6, 3.9); aim(cam, (0, 0, 1.2)); render('gold_oil', sc)


def cyber():
    sc, cam = base_scene()
    bpy.ops.mesh.primitive_cylinder_add(vertices=6, radius=1.5, depth=0.4, location=(-0.6, 0, 1.8), rotation=(math.radians(90), 0, 0))
    o = bpy.context.object; o.scale = (1, 1.25, 1); put(o, mat('navy', 0.3, 0.35), 0.08)
    box((-0.6, -0.3, 1.55), (1.1, 0.25, 0.9), mat('gold', 0.9, 0.25), 0.08)               # 자물쇠 몸통
    bpy.ops.mesh.primitive_torus_add(location=(-0.6, -0.3, 2.1), rotation=(math.radians(90), 0, 0), major_radius=0.38, minor_radius=0.08)
    put(bpy.context.object, mat('steel', 0.9, 0.2))
    cyl((-0.6, -0.45, 1.6), 0.09, 0.1, mat('ink'), rot=(math.radians(90), 0, 0))
    import random; random.seed(11)
    for i in range(14):                                                                     # 데이터 블록
        box((random.uniform(1.2, 3.4), random.uniform(-0.6, 1.2), random.uniform(0.15, 0.4)), (0.3, 0.3, 0.3), mat(random.choice(['teal', 'white', 'coral'])), 0.04)
    arrow((2.1, 0.0, 1.0), (2.7, -0.2, 3.6), 0.13, mat('coral'))
    cam.location = (0.3, -9.4, 4.0); aim(cam, (0.2, 0, 1.5)); render('cyber', sc)


def d1120_top():  # 2026-11-20 1면: 앤트로픽 상장 축포 vs S&P 500 6일 연속 하락 계단
    sc, cam = base_scene()
    sc.render.resolution_x, sc.render.resolution_y = 1200, 750
    # 오른쪽: 6칸 내려가는 계단(6거래일)
    for i in range(6):
        h = 2.9 - i * 0.42
        box((0.6 + i * 0.62, 0.4, h / 2), (0.58, 1.6, h), mat('navy' if i < 5 else 'coral', 0.1, 0.4), 0.04)
    arrow((0.9, -0.7, 3.6), (4.2, -0.9, 1.0), 0.12, mat('coral'))
    # 왼쪽: 받침대 위로 솟는 로켓(상장 첫날 급등)
    box((-2.6, 0.2, 0.3), (1.6, 1.6, 0.6), mat('white'), 0.06)
    cyl((-2.6, 0.2, 2.0), 0.42, 2.2, mat('white', rough=0.3))
    cone((-2.6, 0.2, 3.45), 0.42, 0.0, 0.75, mat('gold', 0.9, 0.2))
    for a in range(3):
        ang = a * 2.094
        box((-2.6 + 0.45 * math.cos(ang), 0.2 + 0.45 * math.sin(ang), 1.1), (0.08, 0.5, 0.7), mat('coral'), 0.02, rot=(0, 0, ang))
    cyl((-2.6, 0.2, 2.35), 0.2, 0.06, mat('blue'), rot=(math.radians(90), 0, 0))
    cone((-2.6, 0.2, 0.75), 0.28, 0.05, 0.5, mat('gold', 0.0, 0.5, 2.5), rot=(math.radians(180), 0, 0))
    import random; random.seed(20)
    for i in range(40):  # 색종이
        x, z = random.uniform(-4.6, -0.8), random.uniform(1.2, 5.0)
        if abs(x + 2.6) < 0.7 and z < 3.9: continue
        box((x, random.uniform(-0.4, 1.4), z), (0.2, 0.04, 0.13), mat(random.choice(['coral', 'gold', 'teal'])), 0.0,
            rot=(random.uniform(0, 3), random.uniform(0, 3), random.uniform(0, 3)))
    cam.location = (0.2, -12.5, 4.6); cam.data.lens = 44; aim(cam, (0.2, 0.2, 2.0)); render('d1120_top', sc)


def stairs():  # 연속 하락 계단(지수 며칠째 하락)
    sc, cam = base_scene()
    for i in range(6):
        h = 3.0 - i * 0.45
        box((-1.6 + i * 0.66, 0.3, h / 2), (0.6, 1.4, h), mat('white' if i < 5 else 'navy', 0.0, 0.5), 0.04)
    sphere((-1.6, 0.3, 3.25), 0.25, mat('coral'))
    arrow((-1.2, -0.8, 3.6), (2.4, -1.0, 0.9), 0.12, mat('navy'))
    cam.location = (0.3, -9.6, 4.2); aim(cam, (0.0, 0.3, 1.6)); render('stairs', sc)


SCENES = {'cyber': cyber, 'nvda': nvda, 'fed': fed, 'ipo': ipo, 'health': health, 'memory': memory, 'gold_oil': gold_oil, 'd1120_top': d1120_top, 'stairs': stairs}
for k, f in SCENES.items():
    if not ONLY or k in ONLY: f()
