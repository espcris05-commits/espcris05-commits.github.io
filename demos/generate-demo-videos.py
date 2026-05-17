#!/usr/bin/env python3
"""
Generate PRO demo videos for Zero MX (zeromx.lat)
WhatsApp-style animations simulating automated customer flows.

Generates individual frames as PNG images, then compiles to MP4 with ffmpeg.
"""

import subprocess, os, shutil, json, textwrap
from PIL import Image, ImageDraw, ImageFont
from math import sin, cos, pi

OUT = "/tmp/zeromx-videos/frames"
os.makedirs(OUT, exist_ok=True)

# --- WhatsApp-style colors ---
WHATSAPP_GREEN  = "#25D366"
WHATSAPP_DARK   = "#075E54"
WHATSAPP_LIGHT  = "#DCF8C6"
WHATSAPP_BG     = "#ECE5DD"
WHATSAPP_HEADER = "#075E54"
TEXT_DARK       = "#1a1a1a"
TEXT_GRAY       = "#667781"
TEXT_WHITE      = "#ffffff"
ACCENT_BLUE     = "#2563eb"
BOT_BUBBLE      = "#2563eb"    # Zero MX bot color
CLIENT_BUBBLE   = "#ffffff"

# --- Dimensions (540x960 = 9:16 phone portrait) ---
W, H = 540, 960

# Fonts
FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_REG  = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

def load_font(size):
    return ImageFont.truetype(FONT_REG, size)

def load_font_bold(size):
    return ImageFont.truetype(FONT_BOLD, size)

def make_phone_frame():
    """Create a base WhatsApp-simulated phone frame."""
    img = Image.new('RGB', (W, H), "#f0f2f5")
    draw = ImageDraw.Draw(img)
    
    # Status bar area
    draw.rectangle([(0,0), (W, 30)], fill=WHATSAPP_HEADER)
    draw.text((20, 6), "📶   📶   🔋", font=load_font(11), fill=TEXT_WHITE)
    draw.text((W-60, 6), "12:00", font=load_font_bold(12), fill=TEXT_WHITE)
    
    # Header bar (contact info)
    draw.rectangle([(0, 30), (W, 80)], fill=WHATSAPP_HEADER)
    # Back arrow
    draw.text((12, 46), "←", font=load_font(20), fill=TEXT_WHITE)
    # Avatar circle
    draw.ellipse([(44, 40), (74, 70)], fill=ACCENT_BLUE)
    draw.text((50, 46), "Z", font=load_font_bold(18), fill=TEXT_WHITE)
    # Contact name
    draw.text((84, 45), "Zero MX — Bot", font=load_font_bold(15), fill=TEXT_WHITE)
    draw.text((84, 63), "en línea", font=load_font(11), fill="#a8d8ea")
    # 3-dot menu
    draw.text((W-34, 46), "⋮", font=load_font(20), fill=TEXT_WHITE)
    
    # Chat area background
    draw.rectangle([(0, 80), (W, H-60)], fill=WHATSAPP_BG)
    
    # Bottom input bar
    draw.rectangle([(0, H-60), (W, H)], fill="#f0f2f5")
    draw.rectangle([(10, H-50), (W-60, H-10)], fill=TEXT_WHITE, outline="#e0e0e0")
    draw.text((18, H-45), "Escribe un mensaje...", font=load_font(13), fill=TEXT_GRAY)
    # Mic icon
    draw.rounded_rectangle([(W-54, H-50), (W-16, H-10)], radius=20, fill=WHATSAPP_GREEN)
    draw.text((W-40, H-44), "🎤", font=load_font(18), fill=TEXT_WHITE)
    
    return img, draw

def draw_bubble(draw, x, y, text, w, is_bot=True, font_size=14):
    """Draw a WhatsApp-style chat bubble."""
    font = load_font(font_size)
    lines = text.split('\n')
    line_h = font_size + 6
    
    # Calculate bubble width from longest line
    max_line_w = max(font.getbbox(l)[2] for l in lines) + 28
    bubble_w = min(max(max_line_w, 60), W - 60)
    bubble_h = len(lines) * line_h + 16
    
    if is_bot:
        # Bot bubble (right-aligned, blue)
        bx = W - bubble_w - 16
        bcolor = BOT_BUBBLE
        tcolor = TEXT_WHITE
        draw.rounded_rectangle([(bx, y), (bx+bubble_w, y+bubble_h)], radius=8, fill=bcolor)
        # Tail
        draw.polygon([(bx+bubble_w-8, y+bubble_h), (bx+bubble_w+4, y+bubble_h), (bx+bubble_w-8, y+bubble_h-8)], fill=bcolor)
    else:
        # Client bubble (left-aligned, white)
        bx = 16
        bcolor = CLIENT_BUBBLE
        tcolor = TEXT_DARK
        draw.rounded_rectangle([(bx, y), (bx+bubble_w, y+bubble_h)], radius=8, fill=bcolor, outline="#e0e0e0")
        draw.polygon([(bx+8, y+bubble_h), (bx-4, y+bubble_h), (bx+8, y+bubble_h-8)], fill=bcolor)
    
    # Draw text
    for i, line in enumerate(lines):
        lw = font.getbbox(line)[2]
        tx = bx + 14
        ty = y + 8 + i * line_h
        draw.text((tx, ty), line, font=font, fill=tcolor)
    
    return y + bubble_h + 6

def draw_typing_indicator(draw, y):
    """Draw typing indicator (3 dots bouncing)."""
    bx = W - 80
    bw = 64
    bh = 36
    draw.rounded_rectangle([(bx, y), (bx+bw, y+bh)], radius=16, fill=BOT_BUBBLE)
    draw.polygon([(bx+bw-6, y+bh), (bx+bw+3, y+bh), (bx+bw-6, y+bh-6)], fill=BOT_BUBBLE)
    # 3 dots
    for i in range(3):
        draw.ellipse([(bx+14+i*16, y+12), (bx+20+i*16, y+18)], fill="white")
    return y + bh + 6

def draw_options_buttons(draw, y, options):
    """Draw quick-reply buttons."""
    bx = W - 16
    y_offset = y
    for opt in options:
        font = load_font(11)
        tw = font.getbbox(opt)[2] + 24
        btn_w = min(tw, W - 36)
        btn_x = W - btn_w - 16
        draw.rounded_rectangle([(btn_x, y_offset), (btn_x+btn_w, y_offset+34)], radius=17, fill="#ffffff", outline=WHATSAPP_GREEN)
        draw.text((btn_x+12, y_offset+8), opt, font=font, fill=WHATSAPP_GREEN)
        y_offset += 40
    return y_offset

def draw_time(draw, x, y, time_str):
    """Draw small timestamp under bubble."""
    draw.text((x, y), time_str, font=load_font(9), fill=TEXT_GRAY)

def draw_info_bar(draw, text_lines):
    """Draw a system notification bar."""
    draw.rectangle([(0, 80), (W, 80)], fill=WHATSAPP_BG)
    y = 84
    for line in text_lines:
        draw.text((W//2 - 100, y), line, font=load_font(12), fill="#155724")
        y += 16

def create_scene_sequence(scene_name, frames_data, fps=30):
    """Generate frames for a scene and return output MP4 path."""
    scene_dir = os.path.join(OUT, scene_name)
    if os.path.exists(scene_dir):
        shutil.rmtree(scene_dir)
    os.makedirs(scene_dir)
    
    frame_num = 0
    for frame_def in frames_data:
        duration = frame_def.get("duration", 30)  # frames
        for _ in range(duration):
            img, draw = make_phone_frame()
            
            # System info bar at top
            if "info" in frame_def:
                draw.text((W//2 - 120, 84), frame_def["info"], font=load_font(11), fill="#155724")
            
            # Draw bubbles
            y_start = 90
            y = y_start
            if "bubbles" in frame_def:
                for b in frame_def["bubbles"]:
                    y = draw_bubble(draw, 0, y, b["text"], 0, is_bot=b.get("bot", True), font_size=b.get("size", 14))
                    if "time" in b:
                        draw_time(draw, W-70 if b.get("bot", True) else 40, y, b["time"])
            
            # Typing indicator
            if "typing" in frame_def:
                y = draw_typing_indicator(draw, y)
            
            # Options buttons
            if "options" in frame_def:
                y = draw_options_buttons(draw, y, frame_def["options"])
            
            # Gradient overlay for transitions
            if "overlay" in frame_def:
                overlay = Image.new('RGBA', (W, H), (0,0,0,0))
                o_draw = ImageDraw.Draw(overlay)
                o_draw.rectangle([(0,0), (W, H)], fill=(0,0,0, frame_def["overlay"]))
                img = Image.alpha_composite(img.convert('RGBA'), overlay).convert('RGB')
            
            # Big title overlay for intro/outro
            if "title" in frame_def:
                overlay = Image.new('RGBA', (W, H), (0,0,0,0))
                o_draw = ImageDraw.Draw(overlay)
                # Semi-transparent dark background
                o_draw.rectangle([(0,0), (W, H)], fill=(0,0,0, 160))
                # Title
                title_font = load_font_bold(frame_def.get("title_size", 28))
                tw = title_font.getbbox(frame_def["title"])[2]
                o_draw.text(((W-tw)//2, H//2 - 40), frame_def["title"], font=title_font, fill=TEXT_WHITE)
                # Subtitle
                if "subtitle" in frame_def:
                    sub_font = load_font(18)
                    sw = sub_font.getbbox(frame_def["subtitle"])[2]
                    o_draw.text(((W-sw)//2, H//2 + 15), frame_def["subtitle"], font=sub_font, fill="#a0a0a0")
                img = Image.alpha_composite(img.convert('RGBA'), overlay).convert('RGB')
            
            # Save frame
            frame_path = os.path.join(scene_dir, f"frame_{frame_num:05d}.png")
            img.save(frame_path)
            frame_num += 1
    
    # Compile to video
    mp4_path = os.path.join(OUT, f"{scene_name}.mp4")
    cmd = [
        "ffmpeg", "-y",
        "-framerate", str(fps),
        "-i", f"{scene_dir}/frame_%05d.png",
        "-c:v", "libx264",
        "-preset", "medium",
        "-crf", "18",
        "-pix_fmt", "yuv420p",
        "-vf", f"scale=540:960:force_original_aspect_ratio=decrease,pad=540:960:(ow-iw)/2:(oh-ih)/2",
        mp4_path
    ]
    subprocess.run(cmd, capture_output=True)
    return mp4_path

# ============================================================
# VIDEO 1: Menú Digital WhatsApp (30-45s)
# ============================================================
def video_menu_digital():
    frames = []
    fps = 24
    
    # Scene 1: Intro title (2s)
    for i in range(fps * 2):
        frames.append({
            "title": "🍽️ Menú Digital",
            "subtitle": "Tus clientes piden desde WhatsApp",
            "title_size": 34,
            "duration": 1
        })
    
    # Scene 2: Client writes first message (3s)
    for i in range(fps * 1):
        frames.append({
            "bubbles": [],
            "duration": 1
        })
    for i in range(fps * 1):
        frames.append({
            "bubbles": [{"text": "¡Buenos días! ¿tienen menú?", "bot": False, "time": "9:05 AM"}],
            "duration": 1
        })
    
    # Scene 3: Bot typing + responds with menu (3s)
    for i in range(fps * 1):
        frames.append({
            "bubbles": [{"text": "¡Buenos días! ¿tienen menú?", "bot": False, "time": "9:05 AM"}],
            "typing": True,
            "duration": 1
        })
    
    # Bot responds with menu (4s)
    menu_text = "🍽️ ¡Claro! Hoy tenemos:\n\n🌮 Tacos de asada - $80\n🥗 Ensalada César - $65\n🍔 Hamburguesa Zero - $95\n🌯 Burrito de pollo - $75\n🥤 Refresco - $25\n\n¿Qué se te antoja? 😊"
    for i in range(fps * 4):
        frames.append({
            "bubbles": [
                {"text": "¡Buenos días! ¿tienen menú?", "bot": False, "time": "9:05 AM"},
                {"text": menu_text, "bot": True, "time": "9:05 AM"}
            ],
            "duration": 1
        })
    
    # Scene 4: Client selects item (2s)
    for i in range(fps * 2):
        frames.append({
            "bubbles": [
                {"text": "¡Buenos días! ¿tienen menú?", "bot": False, "time": "9:05 AM"},
                {"text": menu_text, "bot": True, "time": "9:05 AM"},
                {"text": "La hamburguesa Zero se ve bien, pero ¿trae papas?", "bot": False, "time": "9:06 AM"}
            ],
            "duration": 1
        })
    
    # Scene 5: Bot clarifies + upsells (3s)
    for i in range(fps * 1):
        frames.append({
            "bubbles": [
                {"text": "¡Buenos días! ¿tienen menú?", "bot": False, "time": "9:05 AM"},
                {"text": menu_text, "bot": True, "time": "9:05 AM"},
                {"text": "La hamburguesa Zero se ve bien, pero ¿trae papas?", "bot": False, "time": "9:06 AM"},
            ],
            "typing": True,
            "duration": 1
        })
    
    for i in range(fps * 3):
        frames.append({
            "bubbles": [
                {"text": "¡Buenos días! ¿tienen menú?", "bot": False, "time": "9:05 AM"},
                {"text": menu_text, "bot": True, "time": "9:05 AM"},
                {"text": "La hamburguesa Zero se ve bien, pero ¿trae papas?", "bot": False, "time": "9:06 AM"},
                {"text": "¡Sí! ✅ Viene con papas gajo y salsa de la casa.\n\n🔥 ¿Quieres agregar queso extra (+$15)?", "bot": True, "time": "9:06 AM"}
            ],
            "duration": 1
        })
    
    # Scene 6: Order confirmation (3s)
    for i in range(fps * 1):
        frames.append({
            "bubbles": [
                {"text": "¡Buenos días! ¿tienen menú?", "bot": False, "time": "9:05 AM"},
                {"text": menu_text, "bot": True, "time": "9:05 AM"},
                {"text": "La hamburguesa Zero se ve bien, pero ¿trae papas?", "bot": False, "time": "9:06 AM"},
                {"text": "¡Sí! ✅ Viene con papas gajo y salsa de la casa.\n\n🔥 ¿Quieres agregar queso extra (+$15)?", "bot": True, "time": "9:06 AM"},
                {"text": "Sí, con queso extra porfa", "bot": False, "time": "9:07 AM"}
            ],
            "typing": True,
            "duration": 1
        })
    
    for i in range(fps * 3):
        frames.append({
            "bubbles": [
                {"text": "¡Buenos días! ¿tienen menú?", "bot": False, "time": "9:05 AM"},
                {"text": menu_text, "bot": True, "time": "9:05 AM"},
                {"text": "La hamburguesa Zero se ve bien, pero ¿trae papas?", "bot": False, "time": "9:06 AM"},
                {"text": "¡Sí! ✅ Viene con papas gajo y salsa de la casa.\n\n🔥 ¿Quieres agregar queso extra (+$15)?", "bot": True, "time": "9:06 AM"},
                {"text": "Sí, con queso extra porfa", "bot": False, "time": "9:07 AM"},
                {"text": "✅ ¡Pedido confirmado!\n\n🍔 Hamburguesa Zero c/queso - $110\n📍 Recoger en: Av. Siempre Viva 123\n⏰ Tiempo estimado: 15 min\n\nGracias por tu pedido 🙌", "bot": True, "time": "9:07 AM"}
            ],
            "duration": 1
        })
    
    # Scene 7: Closing with CTA (4s)
    for i in range(fps * 4):
        frames.append({
            "title": "🍽️ Menú Digital Automático",
            "subtitle": "Tus clientes piden sin esperar",
            "title_size": 32,
            "duration": 1
        })
    
    for i in range(fps * 3):
        frames.append({
            "title": "⚡ Zero MX",
            "subtitle": "wa.me/5215512299225",
            "title_size": 34,
            "duration": 1
        })
    
    return create_scene_sequence("demo-menu-digital", frames, fps)

# ============================================================
# VIDEO 2: Reservaciones Automáticas (30-45s)
# ============================================================
def video_reservaciones():
    frames = []
    fps = 24
    
    # Title intro
    for i in range(fps * 2):
        frames.append({
            "title": "📅 Reservaciones Automáticas",
            "subtitle": "Tus clientes reservan 24/7",
            "title_size": 32,
            "duration": 1
        })
    
    # Client: requests reservation
    for i in range(fps * 1):
        frames.append({"bubbles": [], "duration": 1})
    for i in range(fps * 1):
        frames.append({
            "bubbles": [{"text": "Hola, quiero hacer una reservación para hoy", "bot": False, "time": "2:30 PM"}],
            "duration": 1
        })
    
    # Bot typing + asks details
    for i in range(fps * 1):
        frames.append({
            "bubbles": [{"text": "Hola, quiero hacer una reservación para hoy", "bot": False, "time": "2:30 PM"}],
            "typing": True,
            "duration": 1
        })
    
    for i in range(fps * 3):
        frames.append({
            "bubbles": [
                {"text": "Hola, quiero hacer una reservación para hoy", "bot": False, "time": "2:30 PM"},
                {"text": "¡Claro! Encantado de ayudarte 🙌\n\nPara reservar necesito:\n\n1️⃣ ¿A qué hora?\n2️⃣ ¿Cuántas personas?\n3️⃣ ¿Nombre para la reserva?\n4️⃣ ¿Requieres algo especial? 🥳", "bot": True, "time": "2:30 PM"}
            ],
            "duration": 1
        })
    
    # Client provides info
    for i in range(fps * 2):
        frames.append({
            "bubbles": [
                {"text": "Hola, quiero hacer una reservación para hoy", "bot": False, "time": "2:30 PM"},
                {"text": "¡Claro! Encantado de ayudarte 🙌\n\nPara reservar necesito:\n\n1️⃣ ¿A qué hora?\n2️⃣ ¿Cuántas personas?\n3️⃣ ¿Nombre para la reserva?\n4️⃣ ¿Requieres algo especial? 🥳", "bot": True, "time": "2:30 PM"},
                {"text": "A las 8pm, 4 personas, nombre: María García, sin nada especial", "bot": False, "time": "2:31 PM"}
            ],
            "duration": 1
        })
    
    # Bot typing + confirmation
    for i in range(fps * 1):
        frames.append({
            "bubbles": [
                {"text": "Hola, quiero hacer una reservación para hoy", "bot": False, "time": "2:30 PM"},
                {"text": "¡Claro! Encantado de ayudarte 🙌\n\nPara reservar necesito:\n\n1️⃣ ¿A qué hora?\n2️⃣ ¿Cuántas personas?\n3️⃣ ¿Nombre para la reserva?\n4️⃣ ¿Requieres algo especial? 🥳", "bot": True, "time": "2:30 PM"},
                {"text": "A las 8pm, 4 personas, nombre: María García, sin nada especial", "bot": False, "time": "2:31 PM"}
            ],
            "typing": True,
            "duration": 1
        })
    
    for i in range(fps * 4):
        frames.append({
            "bubbles": [
                {"text": "Hola, quiero hacer una reservación para hoy", "bot": False, "time": "2:30 PM"},
                {"text": "¡Claro! Encantado de ayudarte 🙌\n\nPara reservar necesito:\n\n1️⃣ ¿A qué hora?\n2️⃣ ¿Cuántas personas?\n3️⃣ ¿Nombre para la reserva?\n4️⃣ ¿Requieres algo especial? 🥳", "bot": True, "time": "2:30 PM"},
                {"text": "A las 8pm, 4 personas, nombre: María García, sin nada especial", "bot": False, "time": "2:31 PM"},
                {"text": "✅ ¡Reserva confirmada!\n\n📅 Hoy — 8:00 PM\n👥 4 personas\n👤 María García\n📍 Av. Siempre Viva 123\n\nTe enviaremos un recordatorio 1h antes ⏰\n\n¿Algo más? 😊", "bot": True, "time": "2:31 PM"}
            ],
            "duration": 1
        })
    
    # Bot sends reminder (next scene with time change)
    for i in range(fps * 3):
        frames.append({
            "bubbles": [
                {"text": "✅ ¡Reserva confirmada!\n\n📅 Hoy — 8:00 PM\n👥 4 personas\n👤 María García\n📍 Av. Siempre Viva 123\n\nTe enviaremos un recordatorio 1h antes ⏰\n\n¿Algo más? 😊", "bot": True, "time": "2:31 PM"},
                {"text": "⏰ ¡Recordatorio!\n\nTu reserva es en 1 hora\n📅 Hoy — 8:00 PM\n👥 4 personas\n\nTe esperamos 🙌\n\n¿Necesitas algo? Responde aquí y te atenderemos.", "bot": True, "time": "7:00 PM"}
            ],
            "duration": 1
        })
    
    # Closing
    for i in range(fps * 4):
        frames.append({
            "title": "📅 Reservas 24/7",
            "subtitle": "Sin llamadas, sin esperas",
            "title_size": 32,
            "duration": 1
        })
    
    for i in range(fps * 3):
        frames.append({
            "title": "⚡ Zero MX",
            "subtitle": "wa.me/5215512299225",
            "title_size": 34,
            "duration": 1
        })
    
    return create_scene_sequence("demo-reservaciones", frames, fps)

# ============================================================
# VIDEO 3: Captura de Leads (30-45s)
# ============================================================
def video_captura_leads():
    frames = []
    fps = 24
    
    # Title
    for i in range(fps * 2):
        frames.append({
            "title": "🎯 Captura de Leads Automática",
            "subtitle": "Nunca pierdas un cliente potencial",
            "title_size": 30,
            "duration": 1
        })
    
    # Client asks about prices/hours
    for i in range(fps * 1):
        frames.append({"bubbles": [], "duration": 1})
    for i in range(fps * 1):
        frames.append({
            "bubbles": [{"text": "Hola, ¿cuánto cuesta el servicio de catering para 50 personas?", "bot": False, "time": "3:15 PM"}],
            "duration": 1
        })
    
    # Bot asks for contact info first
    for i in range(fps * 1):
        frames.append({
            "bubbles": [{"text": "Hola, ¿cuánto cuesta el servicio de catering para 50 personas?", "bot": False, "time": "3:15 PM"}],
            "typing": True,
            "duration": 1
        })
    
    for i in range(fps * 3):
        frames.append({
            "bubbles": [
                {"text": "Hola, ¿cuánto cuesta el servicio de catering para 50 personas?", "bot": False, "time": "3:15 PM"},
                {"text": "¡Hola! 🙌 Me encantaría darte una cotización.\n\nAntes, ¿me ayudas con estos datos?\n\n📝 Nombre:\n📞 Teléfono:\n📍 Zona/Colonia:\n📅 ¿Para qué fecha?\n\nAsí te paso la info exacta 😊", "bot": True, "time": "3:15 PM"}
            ],
            "duration": 1
        })
    
    # Client provides info
    for i in range(fps * 2):
        frames.append({
            "bubbles": [
                {"text": "Hola, ¿cuánto cuesta el servicio de catering para 50 personas?", "bot": False, "time": "3:15 PM"},
                {"text": "¡Hola! 🙌 Me encantaría darte una cotización.\n\nAntes, ¿me ayudas con estos datos?\n\n📝 Nombre:\n📞 Teléfono:\n📍 Zona/Colonia:\n📅 ¿Para qué fecha?\n\nAsí te paso la info exacta 😊", "bot": True, "time": "3:15 PM"},
                {"text": "Claro, soy Juan Pérez, 555-123-4567, Colonia Centro, para el 25 de mayo", "bot": False, "time": "3:16 PM"}
            ],
            "duration": 1
        })
    
    # Bot processes + saves to CRM
    for i in range(fps * 1):
        frames.append({
            "bubbles": [
                {"text": "Hola, ¿cuánto cuesta el servicio de catering para 50 personas?", "bot": False, "time": "3:15 PM"},
                {"text": "¡Hola! 🙌 Me encantaría darte una cotización.\n\nAntes, ¿me ayudas con estos datos?\n\n📝 Nombre:\n📞 Teléfono:\n📍 Zona/Colonia:\n📅 ¿Para qué fecha?\n\nAsí te paso la info exacta 😊", "bot": True, "time": "3:15 PM"},
                {"text": "Claro, soy Juan Pérez, 555-123-4567, Colonia Centro, para el 25 de mayo", "bot": False, "time": "3:16 PM"}
            ],
            "typing": True,
            "duration": 1
        })
    
    for i in range(fps * 4):
        frames.append({
            "bubbles": [
                {"text": "Hola, ¿cuánto cuesta el servicio de catering para 50 personas?", "bot": False, "time": "3:15 PM"},
                {"text": "¡Hola! 🙌 Me encantaría darte una cotización.\n\nAntes, ¿me ayudas con estos datos?\n\n📝 Nombre:\n📞 Teléfono:\n📍 Zona/Colonia:\n📅 ¿Para qué fecha?\n\nAsí te paso la info exacta 😊", "bot": True, "time": "3:15 PM"},
                {"text": "Claro, soy Juan Pérez, 555-123-4567, Colonia Centro, para el 25 de mayo", "bot": False, "time": "3:16 PM"},
                {"text": "✅ ¡Gracias Juan! Tu info ha sido registrada.\n\nAquí va tu cotización:\n\n🍽️ Catering 50 personas: $18,500 MXN\n📦 Incluye: buffet completo + bebidas + postre\n🎁 Bono: servicio de meseros incluido\n\n¿Te interesa? 🤔\n\nEl equipo te contactará en breve para confirmar.", "bot": True, "time": "3:16 PM"}
            ],
            "duration": 1
        })
    
    # Show notification to owner
    for i in range(fps * 3):
        frames.append({
            "bubbles": [
                {"text": "✅ ¡Gracias Juan! Tu info ha sido registrada.\n\nAquí va tu cotización:\n\n🍽️ Catering 50 personas: $18,500 MXN\n📦 Incluye: buffet completo + bebidas + postre\n🎁 Bono: servicio de meseros incluido\n\n¿Te interesa? 🤔\n\nEl equipo te contactará en breve para confirmar.", "bot": True, "time": "3:16 PM"},
                {"text": "✅ Cliente capturado en CRM\n\n👤 Juan Pérez\n📞 555-123-4567\n📍 Colonia Centro\n📅 Evento: 25 mayo\n💵 Cotización: $18,500 MXN\n\nNotificación enviada al dueño 📲", "bot": True, "time": "3:16 PM"}
            ],
            "duration": 1
        })
    
    # Closing with stats
    for i in range(fps * 3):
        frames.append({
            "title": "🔔 El dueño recibe notificación",
            "subtitle": "Leads capturados SIN perder tiempo",
            "title_size": 28,
            "duration": 1
        })
    
    for i in range(fps * 4):
        frames.append({
            "title": "🎯 Captura Leads Automática",
            "subtitle": "Convierte preguntas en clientes",
            "title_size": 30,
            "duration": 1
        })
    
    for i in range(fps * 3):
        frames.append({
            "title": "⚡ Zero MX",
            "subtitle": "wa.me/5215512299225",
            "title_size": 34,
            "duration": 1
        })
    
    return create_scene_sequence("demo-captura-leads", frames, fps)


# ============================================================
# MAIN
# ============================================================
if __name__ == "__main__":
    import sys
    videos = {
        "menu": video_menu_digital,
        "reservaciones": video_reservaciones,
        "captura": video_captura_leads,
    }
    
    if len(sys.argv) > 1:
        selected = sys.argv[1]
        if selected in videos:
            print(f"Generating video: {selected}...")
            path = videos[selected]()
            print(f"✅ {selected}: {path}")
        else:
            print(f"Unknown video: {selected}. Options: {list(videos.keys())}")
    else:
        for name, fn in videos.items():
            print(f"\n{'='*50}")
            print(f"Generating video: {name}...")
            print("="*50)
            path = fn()
            print(f"✅ {name}: {path}")
    
    print("\n✅ All done!")
