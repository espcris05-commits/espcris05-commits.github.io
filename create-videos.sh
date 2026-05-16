#!/bin/bash
# Crear videos demo mejorados para Cero MX
set -e

cd /tmp/zeromx-page/demos

# ====== VIDEO 1: WhatsApp Bot Demo ======
ffmpeg -y -f lavfi -i "color=c=#dbeafe:s=854x480:d=6" \
  -vf "
    drawtext=text='Cero MX':fontcolor=#2563eb:fontsize=36:fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf:x=(w-text_w)/2:y=30:enable='between(t,0,6)',
    drawtext=text='Bot WhatsApp en accion':fontcolor=#1e293b:fontsize=28:fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf:x=(w-text_w)/2:y=90:enable='between(t,0,2.5)',
    drawtext=text='Cliente escribe -> Bot responde al instante':fontcolor=#475569:fontsize=20:fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf:x=(w-text_w)/2:y=160:enable='between(t,2.5,4.5)',
    drawtext=text='Califica, agenda y cierra 24/7':fontcolor=#475569:fontsize=20:fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf:x=(w-text_w)/2:y=210:enable='between(t,4.5,6)',
    drawtext=text='wa.me/5215512299225':fontcolor=#2563eb:fontsize=18:fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf:x=(w-text_w)/2:y=400:enable='between(t,0,6)',
    drawtext=text='\xF0\x9F\x93\xB1':fontcolor=#2563eb:fontsize=60:x=380:y=260:enable='between(t,0,6)'
  " \
  -c:v libx264 -crf 18 -preset medium -pix_fmt yuv420p \
  whatsapp-bot-demo.mp4

echo "✅ Video 1: whatsapp-bot-demo.mp4"

# ====== VIDEO 2: Landing + WhatsApp ======
ffmpeg -y -f lavfi -i "color=c=#dbeafe:s=854x480:d=6" \
  -vf "
    drawtext=text='Cero MX':fontcolor=#2563eb:fontsize=36:fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf:x=(w-text_w)/2:y=30:enable='between(t,0,6)',
    drawtext=text='Landing Page + WhatsApp':fontcolor=#1e293b:fontsize=28:fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf:x=(w-text_w)/2:y=90:enable='between(t,0,2.5)',
    drawtext=text='Cliente llega a tu pagina web':fontcolor=#475569:fontsize=20:fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf:x=(w-text_w)/2:y=160:enable='between(t,2.5,4)',
    drawtext=text='En 30 segundos ya esta conversando':fontcolor=#475569:fontsize=20:fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf:x=(w-text_w)/2:y=210:enable='between(t,4,6)',
    drawtext=text='wa.me/5215512299225':fontcolor=#2563eb:fontsize=18:fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf:x=(w-text_w)/2:y=400:enable='between(t,0,6)',
    drawtext=text='\xF0\x9F\x8C\x90':fontcolor=#2563eb:fontsize=60:x=380:y=260:enable='between(t,0,6)'
  " \
  -c:v libx264 -crf 18 -preset medium -pix_fmt yuv420p \
  landing-whatsapp-demo.mp4

echo "✅ Video 2: landing-whatsapp-demo.mp4"

# ====== VIDEO 3: AI Sales Assistant ======
ffmpeg -y -f lavfi -i "color=c=#dbeafe:s=854x480:d=6" \
  -vf "
    drawtext=text='Cero MX':fontcolor=#2563eb:fontsize=36:fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf:x=(w-text_w)/2:y=30:enable='between(t,0,6)',
    drawtext=text='Asistente IA para Ventas':fontcolor=#1e293b:fontsize=28:fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf:x=(w-text_w)/2:y=90:enable='between(t,0,2.5)',
    drawtext=text='Un empleado digital que nunca descansa':fontcolor=#475569:fontsize=20:fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf:x=(w-text_w)/2:y=160:enable='between(t,2.5,4)',
    drawtext=text='Vende por ti mientras trabajas en lo tuyo':fontcolor=#475569:fontsize=20:fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf:x=(w-text_w)/2:y=210:enable='between(t,4,6)',
    drawtext=text='wa.me/5215512299225':fontcolor=#2563eb:fontsize=18:fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf:x=(w-text_w)/2:y=400:enable='between(t,0,6)',
    drawtext=text='\xF0\x9F\xA4\x96':fontcolor=#2563eb:fontsize=60:x=380:y=260:enable='between(t,0,6)'
  " \
  -c:v libx264 -crf 18 -preset medium -pix_fmt yuv420p \
  ai-sales-demo.mp4

echo "✅ Video 3: ai-sales-demo.mp4"
echo ""
echo "=== TODOS LOS VIDEOS CREADOS ==="
ls -lh /tmp/zeromx-page/demos/
