from PIL import Image, ImageDraw, ImageFont
import os
PKG=os.path.expanduser("~/workspace/goals/daily-civic-data-brief/hidden_files/nashville-beer-permits-brief-2026-11-06")
src=os.path.join(PKG,"hero_source/media-generation-hero-art-0-7eceeeab-12ec-436d-a21c-093db94abf0a.webp")
img=Image.open(src).convert("RGB"); W,H=img.size
# gradient scrim over top 38%
scrim=Image.new("L",(1,int(H*0.42)),0)
for y in range(int(H*0.42)): scrim.putpixel((0,y), int(200*(1-y/(H*0.42))))
scrim=scrim.resize((W,int(H*0.42)))
black=Image.new("RGB",(W,int(H*0.42)),(18,18,18))
img.paste(Image.composite(black, img.crop((0,0,W,int(H*0.42))), scrim), (0,0))
d=ImageDraw.Draw(img)
def font(sz,bold=True):
    p="/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
    return ImageFont.truetype(p,sz)
x=int(W*0.045)
d.text((x,int(H*0.045)),"22.2%",font=font(int(H*0.115)),fill=(232,163,61))
d.text((x,int(H*0.175)),"of Nashville's issued beer permits sit in",font=font(int(H*0.042)),fill=(245,245,245))
d.text((x,int(H*0.225)),"one council district - District 19 (downtown)",font=font(int(H*0.042)),fill=(245,245,245))
d.text((x,int(H*0.295)),"Nashville Beer Permit Locations register, 2,064 issued permits, snapshot 2026-11-06  |  Machine Readable",font=font(int(H*0.024)),fill=(180,220,215))
img.save(os.path.join(PKG,"hero.png"))
open(os.path.join(PKG,"hero-headline.txt"),"w").write("22.2% of Nashville's issued beer permits sit in one council district - District 19 (downtown)\nSource line: Nashville Beer Permit Locations register, 2,064 issued permits, snapshot 2026-11-06 | Machine Readable\n")
print(img.size)
