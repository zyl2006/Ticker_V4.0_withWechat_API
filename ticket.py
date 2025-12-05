from PIL import Image, ImageDraw, ImageFont
import json, os, random, sys, base64
import qrcode

# ------------------------------
# 字体加载
# ------------------------------
def load_font(font_path, size):
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(__file__))
    if font_path:
        full_path = os.path.join(base_path, font_path)
        if os.path.exists(full_path):
            try: return ImageFont.truetype(full_path, size)
            except: pass
    project_fonts = [
        os.path.join(base_path, "fonts", "TrainTicketFont2.ttf"),
        os.path.join(base_path, "fonts", "simsun.ttc"),
        os.path.join(base_path, "fonts", "simhei.ttf"),
        os.path.join(base_path, "fonts", "times.ttf"),
        os.path.join(base_path, "fonts", "timesbd.ttf"),
        os.path.join(base_path, "fonts", "方正黑体简体.ttf")
    ]
    for p in project_fonts:
        if os.path.exists(p):
            try: return ImageFont.truetype(p, size)
            except: continue
    system_fonts = [r"C:\Windows\Fonts\simhei.ttf", r"C:\Windows\Fonts\times.ttf"]
    for p in system_fonts:
        if os.path.exists(p):
            try: return ImageFont.truetype(p, size)
            except: continue
    return ImageFont.load_default()

# ------------------------------
# 绘制文本
# ------------------------------
def draw_text(draw, text, x, y, font, fill, anchor='la', letter_spacing=0, scale_x=1.0, base_image=None):
    total_width = sum(font.getlength(c) * scale_x + letter_spacing for c in text) - letter_spacing
    if anchor.startswith('r'):
        x -= total_width
    elif anchor.startswith('m'):
        x -= total_width / 2
    for char in text:
        w = font.getlength(char) * scale_x
        if scale_x == 1.0:
            draw.text((x, y), char, font=font, fill=fill)
        else:
            tmp = Image.new('RGBA', (int(font.getlength(char)) + 4, font.size + 4), (0,0,0,0))
            tmp_draw = ImageDraw.Draw(tmp)
            tmp_draw.text((0,0), char, font=font, fill=fill)
            tmp = tmp.resize((max(int(tmp.width*scale_x),1), tmp.height), resample=Image.BICUBIC)
            if base_image: base_image.paste(tmp, (int(x), int(y)), tmp)
        x += w + letter_spacing
    return total_width, font.size

# ------------------------------
# 虚线矩形
# ------------------------------
def draw_dashed_rectangle(draw, xy, dash_length=5, fill='black', width=1):
    x0,y0,x1,y1 = xy
    x=x0
    while x<x1: x_end=min(x+dash_length,x1); draw.line([(x,y0),(x_end,y0)], fill=fill, width=width); x+=2*dash_length
    x=x0
    while x<x1: x_end=min(x+dash_length,x1); draw.line([(x,y1),(x_end,y1)], fill=fill, width=width); x+=2*dash_length
    y=y0
    while y<y1: y_end=min(y+dash_length,y1); draw.line([(x0,y),(x0,y_end)], fill=fill, width=width); y+=2*dash_length
    y=y0
    while y<y1: y_end=min(y+dash_length,y1); draw.line([(x1,y),(x1,y_end)], fill=fill, width=width); y+=2*dash_length

# ------------------------------
# 半尖箭头
# ------------------------------
def draw_half_arrow(draw, xy, length=20, height=10, direction='right', fill='black'):
    x,y=xy
    if direction=='right': points=[(x,y),(x+length,y-height/2),(x+length,y+height/2)]
    elif direction=='left': points=[(x+length,y),(x,y-height/2),(x,y+height/2)]
    elif direction=='up': points=[(x,y+length),(x-height/2,y),(x+height/2,y)]
    elif direction=='down': points=[(x,y),(x-height/2,y+length),(x+height/2,y+length)]
    draw.polygon(points, fill=fill)

# ------------------------------
# 直线
# ------------------------------
def draw_line(draw,start,end,fill='black',width=1): draw.line([start,end],fill=fill,width=width)

# ------------------------------
# 带圈文字
# ------------------------------
def draw_multi_circle_text(draw, xy, text, font, fill="#000000", spacing=10, circle_radius=None, circle_fill=None, width=2):
    if not text: return
    x,y=xy
    char_data=[]
    for ch in text:
        w=font.getlength(ch)
        h=font.size
        r=circle_radius or int(max(w,h)/2+4)
        char_data.append((ch,r))
    total_width=sum(2*r+spacing for _,r in char_data)-spacing
    start_x=x-total_width/2
    cx=start_x
    for ch,r in char_data:
        cx_center=cx+r; cy_center=y
        draw.ellipse([cx_center-r, cy_center-r, cx_center+r, cy_center+r], outline=fill, fill=circle_fill, width=width)
        w=font.getlength(ch)
        draw.text((cx_center-w/2, cy_center-font.size/2), ch, font=font, fill=fill)
        cx+=2*r+spacing

# ------------------------------
# 条码占位
# ------------------------------
def make_barcode_placeholder(data,width,height):
    # Create transparent background and draw opaque black stripes
    im=Image.new('RGBA',(width,height),(255,255,255,0))
    dr=ImageDraw.Draw(im)
    rng=random.Random(hash(data)&0xffffffff)
    x=0
    while x<width:
        wstripe=rng.randint(2,7)
        if rng.random()<0.55:
            dr.rectangle([x,0,x+wstripe,height], fill=(0,0,0,255))
        # else leave transparent
        x+=wstripe
    return im

# ------------------------------
# 二维码
# ------------------------------
def encode_ticket_data(user_data: dict) -> str:
    s=""
    letter=user_data.get("字母"," ").ljust(1)
    s+=f"{ord(letter[0])-39:02d}"
    s+=user_data.get("票号","").rjust(6)
    s+=user_data.get("年","").rjust(4)
    s+=user_data.get("月","").rjust(2)
    s+=user_data.get("日","").rjust(2)
    typ=user_data.get("类型","  ").ljust(2)
    s+=''.join(f"{ord(c)-39:02d}" for c in typ)
    s+=user_data.get("车次号","").rjust(6)
    s+=user_data.get("车厢号","").rjust(4)
    s+=user_data.get("席位号","").rjust(5)
    seat_letter=user_data.get("普通序号"," ").ljust(1)
    s+=f"{ord(seat_letter[0])-39:02d}".ljust(5)
    id_letter=user_data.get("其它证件标识符","  ").ljust(2)
    s+=''.join(f"{ord(c)-39:02d}" for c in id_letter)
    s+=user_data.get("身份证号1","").rjust(10)
    s+=user_data.get("身份证号2","").rjust(5)
    name_b64=base64.b64encode(user_data.get("姓名","").encode("utf-8")).decode("ascii")
    s+=name_b64.ljust(41)
    s+=user_data.get("时","").rjust(2)
    s+=user_data.get("分","").rjust(2)
    return s

def make_qr_from_number_string(data_str:str,size_px:int=280):
    qr=qrcode.QRCode(version=1,error_correction=qrcode.constants.ERROR_CORRECT_L,box_size=6,border=0)
    qr.add_data(data_str)
    qr.make(fit=True)
    qr_img=qr.make_image(fill_color="black", back_color="white").convert("RGBA")
    datas=qr_img.getdata()
    new_data=[]
    for px in datas:
        if px[0]>200 and px[1]>200 and px[2]>200: new_data.append((255,255,255,0))
        else: new_data.append(px)
    qr_img.putdata(new_data)
    if qr_img.width!=size_px or qr_img.height!=size_px: qr_img=qr_img.resize((size_px,size_px), resample=Image.NEAREST)
    return qr_img

# ------------------------------
# 安全映射
# ------------------------------
class SafeDict(dict):
    def __missing__(self,key): return ''

# ------------------------------
# 扁平化字段
# ------------------------------
def flatten_user_data(user_data):
    flat={}
    for k,v in user_data.items():
        if isinstance(v,dict):
            if not v.get("enabled",True): continue
            flat[k]=v.get("value","")
        else:
            flat[k]=v
    return flat

# ------------------------------
# 渲染票
# ------------------------------
def render_ticket(user_data, template_json_path, template_dir, apply_template=False):
    flat=flatten_user_data(user_data)
    normalized={str(k).strip():("" if v is None else str(v)) for k,v in flat.items()}
    fmt_map=SafeDict(normalized)
    def get_val(k):
        if k in flat and flat[k] is not None: return str(flat[k])
        ks=str(k).strip()
        return normalized.get(ks,"")
    with open(template_json_path,'r',encoding='utf-8') as f: cfg=json.load(f)
    bg_path=os.path.join(template_dir,cfg['canvas']['background'])
    base=Image.open(bg_path).convert('RGB')
    dr=ImageDraw.Draw(base)

    apply_template=cfg.get('apply_$',False)
    if apply_template:
        t_img_path="templates/1234.png"
        if os.path.exists(t_img_path):
            t_img=Image.open(t_img_path).convert("RGBA")
            scale=float(cfg.get('apply_$scale',1.0))
            if scale!=1.0:
                t_img=t_img.resize((max(int(t_img.width*scale),1),max(int(t_img.height*scale),1)), resample=Image.BICUBIC)
            base.paste(t_img,(90,460),t_img)

    # 可选渲染箭头图片（保持透明度）
    if cfg.get('apply_arrow', False):
        arrow_path=os.path.join('templates','arrow.png')
        if os.path.exists(arrow_path):
            a_img=Image.open(arrow_path).convert('RGBA')
            a_scale=float(cfg.get('arrow_scale',1.0))
            if a_scale!=1.0:
                a_img=a_img.resize((max(int(a_img.width*a_scale),1),max(int(a_img.height*a_scale),1)), resample=Image.BICUBIC)
            ax=int(cfg.get('arrow_x',0)); ay=int(cfg.get('arrow_y',0))
            base.paste(a_img,(ax,ay),a_img)

    for key,spec in cfg['fields'].items():
        t=spec.get("type")
        if t=="dashed_rect": draw_dashed_rectangle(dr,spec["xy"],spec.get("dash_length",5),spec.get("fill","#000000"),spec.get("width",1)); continue
        if t=="arrow": draw_half_arrow(dr,(spec["x"],spec["y"]),spec.get("length",20),spec.get("height",10),spec.get("direction","right"),spec.get("fill","#000000")); continue
        if t=="line": draw_line(dr,spec["start"],spec["end"],fill=spec.get("fill","#000000"),width=spec.get("width",1)); continue
        if t=="circle_text":
            text=get_val("票种")
            if not text: continue
            font=load_font(spec.get("font_path"),spec.get("size",50))
            fill_color=spec.get("fill","#000000")
            circle_fill=spec.get("fill_circle",None)
            spacing=spec.get("spacing",10)
            circle_radius=spec.get("radius",None)
            width=spec.get("width",3)
            char_data=[]
            for ch in text:
                w=font.getlength(ch);h=font.size
                r=circle_radius or int(max(w,h)/2+4)
                char_data.append((ch,r))
            total_width=sum(2*r+spacing for _,r in char_data)-spacing
            x0,y0=spec["x"],spec["y"];anchor=spec.get("anchor","ma")
            if anchor.startswith("r"): x0-=total_width
            elif anchor.startswith("m"): x0-=total_width/2
            cx=x0
            for ch,r in char_data:
                cx_center=cx+r;cy_center=y0
                dr.ellipse([cx_center-r,cy_center-r,cx_center+r,cy_center+r],outline=fill_color,fill=circle_fill,width=width)
                tw=font.getlength(ch);th=font.size
                dr.text((cx_center-tw/2,cy_center-th/2),ch,font=font,fill=fill_color)
                cx+=2*r+spacing
            continue
        # 兼容模板未显式声明 circle_text 的情况：对“车票类型/票种”强制按带圈文字渲染
        if key in ("车票类型","票种"):
            text=get_val("票种")
            if text:
                # 从字段或其第一个 segment 继承样式
                font_path=spec.get("font_path")
                size=spec.get("size")
                fill_color=spec.get("fill","#000000")
                spacing=spec.get("spacing")
                if (not font_path or not size or spacing is None) and "segments" in spec and spec["segments"]:
                    seg0=spec["segments"][0]
                    font_path=font_path or seg0.get("font_path")
                    size=size or seg0.get("size",50)
                    if spacing is None: spacing=seg0.get("letter_spacing",10)
                    if fill_color=="#000000": fill_color=seg0.get("fill","#000000")
                if spacing is None: spacing=10
                font=load_font(font_path,size or 50)
                circle_fill=spec.get("fill_circle",None)
                circle_radius=spec.get("radius",None)
                width=spec.get("width",3)
                # 准备每字半径，宽度随字符自适应
                char_data=[]
                for ch in text:
                    w=font.getlength(ch);h=font.size
                    r=circle_radius or int(max(w,h)/2+4)
                    char_data.append((ch,r))
                total_width=sum(2*r+spacing for _,r in char_data)-spacing
                x0,y0=spec["x"],spec["y"];anchor=spec.get("anchor","ma")
                if anchor.startswith("r"): x0-=total_width
                elif anchor.startswith("m"): x0-=total_width/2
                cx=x0
                for ch,r in char_data:
                    cx_center=cx+r;cy_center=y0
                    dr.ellipse([cx_center-r,cy_center-r,cx_center+r,cy_center+r],outline=fill_color,fill=circle_fill,width=width)
                    tw=font.getlength(ch);th=font.size
                    dr.text((cx_center-tw/2,cy_center-th/2),ch,font=font,fill=fill_color)
                    cx+=2*r+spacing
                continue
        if key=='二维码':
            data_str=encode_ticket_data(fmt_map)
            qr_img_rgba=make_qr_from_number_string(data_str,spec.get("size",280))
            base.paste(qr_img_rgba,(spec["x"]-qr_img_rgba.width//2,spec["y"]-qr_img_rgba.height//2),qr_img_rgba)
            continue
        if key=='条码':
            bc=make_barcode_placeholder(str(fmt_map.get('条码数据','demo')),spec["width"],spec["height"])
            # preserve transparency by supplying mask
            base.paste(bc,(spec["x"],spec["y"]),bc)
            continue
        text=get_val(key)
        if "segments" in spec:
            # 解析段落文本的工具：支持按用户变量重复字符
            def _resolve_seg_text(seg):
                raw = seg["text"].format_map(fmt_map)
                repeat_char = seg.get("repeat_char")
                repeat_count_key = seg.get("repeat_count_key")
                if repeat_char is not None and repeat_count_key:
                    try:
                        cnt = int(fmt_map.get(repeat_count_key, 0))
                    except:
                        cnt = 0
                    return (repeat_char or "") * max(cnt, 0)
                # 兼容旧模板：若文本全为“*”，使用用户提供的“星号个数”覆盖长度
                if raw and set(raw) == {"*"}:
                    try:
                        cnt = int(fmt_map.get("星号个数", len(raw)))
                    except:
                        cnt = len(raw)
                    return "*" * max(cnt, 0)
                return raw
            x_base=spec["x"];y_base=spec["y"];total_width=0
            for seg in spec["segments"]:
                seg_text=_resolve_seg_text(seg)
                f=load_font(seg.get("font_path",None),seg.get("size",24))
                seg_width=sum(f.getlength(c)+seg.get("letter_spacing",0) for c in seg_text)-seg.get("letter_spacing",0)
                total_width+=seg_width
            if spec.get("anchor","la").startswith('r'): x_base-=total_width
            elif spec.get("anchor","la").startswith('m'): x_base-=total_width/2
            for seg in spec["segments"]:
                seg_text=_resolve_seg_text(seg)
                f=load_font(seg.get("font_path",None),seg.get("size",24))
                draw_text(dr,seg_text,x_base,y_base+seg.get("y_offset",0),f,seg.get("fill","#000000"),anchor='la',letter_spacing=seg.get("letter_spacing",0),scale_x=seg.get("scale_x",1.0),base_image=base)
                w,_=draw_text(dr,seg_text,x_base,y_base+seg.get("y_offset",0),f,seg.get("fill","#000000"),anchor='la',letter_spacing=seg.get("letter_spacing",0),scale_x=seg.get("scale_x",1.0),base_image=base)
                x_base+=w
        else:
            if not text: continue
            f=load_font(spec.get("font_path"),spec.get("size",24))
            draw_text(dr,text,spec["x"],spec["y"],f,spec.get("fill","#000000"),spec.get("anchor","la"),letter_spacing=spec.get("letter_spacing",0),base_image=base)

    return base
