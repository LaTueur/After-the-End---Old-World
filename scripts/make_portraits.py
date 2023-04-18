from PIL import Image, ImageDraw, ImageFilter
import os

SIZE = 152
COUNT = 26

TEMPLATE = """
spriteTypes = [
	spriteType = [
		name = "GFX_portrait_NEOD_portraits_{num}"
		texturefile = "gfx/static_portraits/GFX_portrait_NEOD_portraits_{num}.png"
		noOfFrames = 27
		norefcount = yes
		can_be_lowres = yes
	]
    portraitType = [
        name = "PORTRAIT_NEOD_static_{num}"

        weight = [
            additive_modifier = [
                value = 1000000
                portrait_clothing = yes
				{req}
			]
        ]

        layer = [
            "GFX_empty:c0"
            "GFX_empty:c2"
            "GFX_empty:c3"
            "GFX_empty:c1"
            "GFX_empty:c4"
            "GFX_empty:p1:h:y"
            "GFX_portrait_NEOD_portraits_{num}:c5"
        ]

        allow_property_values = [
            1 = [
				0  = [ always = yes ]
            ]
            19 = [
				0  = [ always = yes ]
            ]
			33 = [
				0  = [ always = yes ]
            ]
            34 = [
				0  = [ always = yes ]
            ]
            35 = [
				0  = [ always = yes ]
            ]
            36 = [
				0  = [ always = yes ]
            ]
			6 = [
				0 = [ always = yes ]
            ]
            5 = [
				0 = [ always = no ]
				{list}
			]
		]
	]
]"""

def crop_center(pil_img, crop_width, crop_height):
    img_width, img_height = pil_img.size
    return pil_img.crop(((img_width - crop_width) // 2,
                         (img_height - crop_height) // 2,
                         (img_width + crop_width) // 2,
                         (img_height + crop_height) // 2))

def crop_max_square(pil_img):
    return crop_center(pil_img, min(pil_img.size), min(pil_img.size))

def process_image(pil_img):
    return crop_max_square(pil_img).resize((152,152))

def get_religions(file_name: str):
    return file_name.split(".")[0].split("+")

def get_id():
    return f"{len(religions):02d}"

def save_big_img():
    Image.composite(big_img, nothing, mask).save(f"../NEOD/gfx/static_portraits/GFX_portrait_NEOD_portraits_{get_id()}.png")

def religion_line(rel):
    return f"portrait_religion = {rel}"

def build_religions(rels):
    if len(rels) == 1:
        return religion_line(rels[0])
    else:
        return f"OR = [{' '.join(map(religion_line, rels))}]"

def save_religions():
    req = build_religions(list(sum(religions[-1], [])))
    ls = "" 
    for i, r in enumerate(religions[-1]):
        ls += f"{i+1} = [{build_religions(r)}]\n"
    for i in range(len(religions[-1]), COUNT):
        ls += f"{i+1} = [ always = no ]\n"
    text = TEMPLATE.format(num=get_id(),req=req, list=ls).replace("[", "{").replace("]", "}")
    file = open(f"../NEOD/interface/portraits/NEOD_static_portraits_{get_id()}.gfx", "w")
    file.write(text)
    file.close()

mask = Image.open('mask.png').convert('L')
nothing = Image.new("RGBA", (SIZE*(COUNT+1), SIZE), 0)
religions = [[]]
big_img = Image.new("RGBA", (SIZE*(COUNT+1), SIZE), 0)
for i, file in enumerate(os.listdir("portraits")):
    if i % COUNT == 0 and i != 0:
        save_religions()
        religions.append([])
        save_big_img()
    img = process_image(Image.open(f'portraits/{file}'))
    religions[-1].append(get_religions(file))
    big_img.paste(img, (SIZE*(i%COUNT+1), 0))

save_religions()
save_big_img()