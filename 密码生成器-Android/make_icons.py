"""生成 Android 各尺寸 PNG 图标"""
import os, struct, zlib

def make_png(size):
    w = h = size
    cx, cy = w // 2, h // 2
    
    BG = (13, 71, 161)   # #0d47a1
    WHITE = (255, 255, 255)
    
    rows = []
    for y in range(h):
        row = [0]  # filter byte
        for x in range(w):
            dx, dy = x - cx, y - cy
            dist = (dx*dx + dy*dy) ** 0.5
            r = w * 0.46
            
            # 圆角矩形背景
            margin = w * 0.08
            in_rect = (margin <= x < w - margin and margin <= y < h - margin)
            corner_r = w * 0.18
            
            def in_rounded_rect():
                if not in_rect:
                    return False
                corners = [
                    (margin + corner_r, margin + corner_r),
                    (w - margin - corner_r, margin + corner_r),
                    (margin + corner_r, h - margin - corner_r),
                    (w - margin - corner_r, h - margin - corner_r),
                ]
                for (cx2, cy2) in corners:
                    if x < cx2 and y < cy2 and (x - cx2)**2 + (y - cy2)**2 > corner_r**2:
                        return False
                    if x >= w - (cx2) and y < cy2 and (x - (w - margin - corner_r))**2 + (y - cy2)**2 > corner_r**2:
                        pass
                return True
            
            is_bg = in_rounded_rect()
            
            if not is_bg:
                row.extend([0, 0, 0, 0])
                continue
            
            # 绘制钥匙图案
            # 钥匙圆头
            key_cx = cx - w * 0.1
            key_cy = cy - h * 0.05
            head_r = w * 0.14
            head_hole_r = w * 0.07
            
            hdx = x - key_cx
            hdy = y - key_cy
            hdist = (hdx*hdx + hdy*hdy) ** 0.5
            
            # 钥匙柄（斜向右下）
            stem_w = w * 0.075
            angle_cos, angle_sin = 0.707, 0.707  # 45度
            # 柄的起点（从圆头右侧出发）
            stem_sx = key_cx + head_r * angle_cos
            stem_sy = key_cy + head_r * angle_sin
            stem_len = w * 0.30
            # 点到线段的距离
            px, py = x - stem_sx, y - stem_sy
            t = (px * angle_cos + py * angle_sin) / stem_len
            t = max(0.0, min(1.0, t))
            nearest_x = stem_sx + t * stem_len * angle_cos
            nearest_y = stem_sy + t * stem_len * angle_sin
            sdist = ((x - nearest_x)**2 + (y - nearest_y)**2) ** 0.5
            in_stem = sdist < stem_w and t > 0
            
            # 钥匙齿
            teeth_start_t = 0.35
            in_tooth1 = in_tooth2 = False
            if t > teeth_start_t:
                # 第一个齿
                t1_center = teeth_start_t + 0.20
                t2_center = teeth_start_t + 0.50
                tooth_len = w * 0.09
                tooth_w = w * 0.065
                # 齿垂直于柄方向
                perp_cos, perp_sin = angle_sin, -angle_cos  # 旋转90度
                for tc in [t1_center, t2_center]:
                    tx = stem_sx + tc * stem_len * angle_cos
                    ty = stem_sy + tc * stem_len * angle_sin
                    tdx = x - tx
                    tdy = y - ty
                    along = tdx * angle_cos + tdy * angle_sin
                    perp  = tdx * perp_cos + tdy * perp_sin
                    if abs(along) < tooth_w and 0 < perp < tooth_len:
                        in_tooth1 = True
            
            in_key = (hdist <= head_r and hdist > head_hole_r) or in_stem or in_tooth1
            
            if in_key:
                row.extend([WHITE[0], WHITE[1], WHITE[2], 255])
            else:
                row.extend([BG[0], BG[1], BG[2], 255])
        rows.append(bytes(row))
    
    raw = b''.join(rows)
    compressed = zlib.compress(raw, 9)
    
    def chunk(name, data):
        c = name + data
        return struct.pack('>I', len(data)) + c + struct.pack('>I', zlib.crc32(c) & 0xffffffff)
    
    ihdr = struct.pack('>II', w, h) + bytes([8, 6, 0, 0, 0])
    
    return (b'\x89PNG\r\n\x1a\n'
            + chunk(b'IHDR', ihdr)
            + chunk(b'IDAT', compressed)
            + chunk(b'IEND', b''))

base = r"C:\Users\lenovo\WorkBuddy\20260330173521\password-android\app\src\main\res"

configs = [
    ("mipmap-mdpi",    48),
    ("mipmap-hdpi",    72),
    ("mipmap-xhdpi",   96),
    ("mipmap-xxhdpi",  144),
    ("mipmap-xxxhdpi", 192),
]

for folder, size in configs:
    path = os.path.join(base, folder)
    os.makedirs(path, exist_ok=True)
    for name in ["ic_launcher.png", "ic_launcher_round.png"]:
        with open(os.path.join(path, name), "wb") as f:
            f.write(make_png(size))
    print(f"  {folder}: {size}x{size}")

print("图标生成完成")
