#!/bin/bash
# Videos demo PRO para Zero MX
set -e

cd /tmp/zeromx-page/demos
FONT_BOLD="/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_REG="/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
W=854
H=480
D=7

# ====== VIDEO 1: WhatsApp Bot ======
ffmpeg -y -f lavfi -i "color=c=#f0f4ff:s=${W}x${H}:d=${D}" \
  -vf "
    drawtext=text='Zero MX':fontcolor=#2563eb:fontsize=40:fontfile=${FONT_BOLD}:x=(w-text_w)/2:y=40:enable='between(t,0,${D})',
    drawtext=text='Bot WhatsApp':fontcolor=#1e293b:fontsize=32:fontfile=${FONT_BOLD}:x=(w-text_w)/2:y=100:enable='between(t,0,2)',
    drawtext=text='Respondemos por ti 24/7':fontcolor=#475569:fontsize=22:fontfile=${FONT_REG}:x=(w-text_w)/2:y=150:enable='between(t,1.5,3.5)',
    drawtext=text='Captura leads mientras duermes':fontcolor=#475569:fontsize=22:fontfile=${FONT_REG}:x=(w-text_w)/2:y=200:enable='between(t,3.5,5.5)',
    drawtext=text='Agenda citas y cobra automatico':fontcolor=#475569:fontsize=22:fontfile=${FONT_REG}:x=(w-text_w)/2:y=250:enable='between(t,5,${D})',
    drawtext=text='wa.me/5215512299225':fontcolor=#2563eb:fontsize=18:fontfile=${FONT_REG}:x=(w-text_w)/2:y=400:enable='between(t,0,${D})',
    drawtext=text='\xF0\x9F\x93\xB1':fontcolor=#2563eb:fontsize=70:x=380:y=290:enable='between(t,0,${D})'
  " \
  -c:v libx264 -crf 18 -preset medium -pix_fmt yuv420p \
  whatsapp-bot-demo.mp4
echo "✅ Video 1: whatsapp-bot-demo.mp4"

# ====== VIDEO 2: Landing Page ======
ffmpeg -y -f lavfi -i "color=c=#f0f4ff:s=${W}x${H}:d=${D}" \
  -vf "
    drawtext=text='Zero MX':fontcolor=#2563eb:fontsize=40:fontfile=${FONT_BOLD}:x=(w-text_w)/2:y=40:enable='between(t,0,${D})',
    drawtext=text='Landing Page + WhatsApp':fontcolor=#1e293b:fontsize=32:fontfile=${FONT_BOLD}:x=(w-text_w)/2:y=100:enable='between(t,0,2)',
    drawtext=text='Cliente llega a tu pagina web':fontcolor=#475569:fontsize=22:fontfile=${FONT_REG}:x=(w-text_w)/2:y=160:enable='between(t,2,3.5)',
    drawtext=text='En 30 segundos ya esta en WhatsApp':fontcolor=#475569:fontsize=22:fontfile=${FONT_REG}:x=(w-text_w)/2:y=210:enable='between(t,3.5,5.5)',
    drawtext=text='Lead capturado sin que hagas nada':fontcolor=#475569:fontsize=22:fontfile=${FONT_REG}:x=(w-text_w)/2:y=260:enable='between(t,5,${D})',
    drawtext=text='wa.me/5215512299225':fontcolor=#2563eb:fontsize=18:fontfile=${FONT_REG}:x=(w-text_w)/2:y=400:enable='between(t,0,${D})',
    drawtext=text='\xF0\x9F\x8C\x90':fontcolor=#2563eb:fontsize=70:x=380:y=290:enable='between(t,0,${D})'
  " \
  -c:v libx264 -crf 18 -preset medium -pix_fmt yuv420p \
  landing-whatsapp-demo.mp4
echo "✅ Video 2: landing-whatsapp-demo.mp4"

# ====== VIDEO 3: AI Sales ======
ffmpeg -y -f lavfi -i "color=c=#f0f4ff:s=${W}x${H}:d=${D}" \
  -vf "
    drawtext=text='Zero MX':fontcolor=#2563eb:fontsize=40:fontfile=${FONT_BOLD}:x=(w-text_w)/2:y=40:enable='between(t,0,${D})',
    drawtext=text='Asistente IA de Ventas':fontcolor=#1e293b:fontsize=32:fontfile=${FONT_BOLD}:x=(w-text_w)/2:y=100:enable='between(t,0,2)',
    drawtext=text='Un empleado digital para tu negocio':fontcolor=#475569:fontsize=22:fontfile=${FONT_REG}:x=(w-text_w)/2:y=160:enable='between(t,2,4)',
    drawtext=text='Califica, negocia y cierra por ti':fontcolor=#475569:fontsize=22:fontfile=${FONT_REG}:x=(w-text_w)/2:y=210:enable='between(t,4,6)',
    drawtext=text='Nunca se cansa, nunca deja de vender':fontcolor=#475569:fontsize=22:fontfile=${FONT_REG}:x=(w-text_w)/2:y=260:enable='between(t,5,${D})',
    drawtext=text='wa.me/5215512299225':fontcolor=#2563eb:fontsize=18:fontfile=${FONT_REG}:x=(w-text_w)/2:y=400:enable='between(t,0,${D})',
    drawtext=text='\xF0\x9F\xA4\x96':fontcolor=#2563eb:fontsize=70:x=380:y=290:enable='between(t,0,${D})'
  " \
  -c:v libx264 -crf 18 -preset medium -pix_fmt yuv420p \
  ai-sales-demo.mp4
echo "✅ Video 3: ai-sales-demo.mp4"

echo ""
echo "=== VIDEOS CREADOS ==="
ls -lh /tmp/zeromx-page/demos/
