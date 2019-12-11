from Config._const import PREFIX
import numpy as np
import os, discord, random, asyncio
from PIL import Image, ImageDraw
from Config._functions import grammar_list

HELP = {
	"MAIN": "Generate a tr_ of random length and compare it to other objects",
	"FORMAT": "",
	"CHANNEL": 0,
	"USAGE": f"""Using `{PREFIX}tr_` will generate a tr_ of random length and draw it accordingly, while also 
	providing a scale reference in the form of an object or organism.""".replace("\n", "").replace("\t", "")
}

PERMS = 0 # Non-members
ALIASES = ["TR_"]
REQ = []

async def MAIN(message, args, level, perms):
	if level != 1:
		if args[1].lower() == "queue" and perms == 2:
			await message.channel.send(open("Config/_tr_gen.txt", "r").read())
			return
	
	tr_gen = open("Config/_tr_gen.txt", "r").read()
	tr_gen += f" {message.id}"
	open("Config/_tr_gen.txt", "w").write(tr_gen.strip())

	while not open("Config/_tr_gen.txt", "r").read().startswith(str(message.id)):
		await asyncio.sleep(1)

	pixel_count = 250 * np.power(2.5, np.random.pareto(1))

	image_pixels = 551 + 115 + pixel_count
	height = (0.2 / 860) * image_pixels

	if height > 10:
		image_pixels = 10 / (0.2 / 860)
		pixel_count = image_pixels - 115 - 551

	top = Image.open("Images/tr_ top.png").convert("RGBA")
	face = Image.open("Images/tr_ face.png").convert("RGBA")
	grad = Image.open("Images/tr_ gradient.png").convert("RGBA")
	bottom = Image.open("Images/tr_ bottom.png").convert("RGBA")

	tr_base = Image.new("RGBA", (1440, int(image_pixels)), (0, 0, 0, 0))
	tr_base.paste(top, (0, 0))
	grad = grad.resize((1440, int(pixel_count)))
	tr_base.paste(grad, (0, 115))
	tr_base.paste(bottom, (0, int(image_pixels)-670), mask=bottom)

	face_position = min(309, 
		int(image_pixels/2) - 343)
	
	tr_base.paste(face, (0, face_position), mask=face)

	ratio = 500 / image_pixels
	
	tr_base = tr_base.resize((int(1440 * ratio), int(image_pixels * ratio)), Image.ANTIALIAS)
	w = 1440 * ratio
	h = int(image_pixels * ratio)

	center_w = max(min(300, 300 / np.sqrt(height)), 70)

	to_post = Image.open("Images/tr_ background.png").convert("RGBA")
	to_post.paste(tr_base, (int(center_w - w/2), 580 - h), mask=tr_base)

	scale_objects = {
		"Tesla Cybertruck": 1.9,
		"Elephant": 3.2,
		"Basketball": 0.23,
		"Human Hand": 0.19,
		"Apple Pro Stand": 0.45,
		"Hummingbird": 0.1,
		"Robert Wadlow": 2.72,
		"Blue Whale": 4.5,
		"Bonsai Tree": 0.8,
		"Four Year Old Child": 1.1,
		"Aegislash": 1.7,
		"Purplegaze": 1.77,
		"Medium Dog House": 0.65,
		"Hedgehog": 0.12,
		"Pine Tree": 15,
		"All Diary of a Wimpy Kid Books Stacked on Top of Each Other": 0.27
	}

	current_w = center_w * 1.65

	pixels_per_height = 500 / height

	references = []
	for scale in scale_objects.keys():
		if 0.2 * height < scale_objects[scale] < 1.15 * height:
			img = Image.open(f"Images/{scale}.png").convert("RGBA")
			ratio = (pixels_per_height * scale_objects[scale]) / img.height
			img = img.resize((int(img.width * ratio), int(img.height * ratio)))

			references.append([scale, img, img.width, img.height])
	
	to_scale = []

	while True:
		possible_ref = []

		for ref in references:
			if ref[2] + current_w <= 1580:
				possible_ref.append(ref)
		
		if len(possible_ref) == 0:
			break

		ref = random.choice(possible_ref)

		to_post.paste(ref[1], (int(current_w), 580 - ref[3]), mask=ref[1])
		current_w += ref[2] + 70

		to_scale.append(f"**`{ref[0]}`** ({scale_objects[ref[0]]}m tall)")
		references.remove(ref)

	if len(to_scale) != 0:
		to_scale = "To scale: " + grammar_list(to_scale)
	else:
		to_scale = ""

	to_post.save("Images/generated tr_.png")

	width_note = ""
	if height >= 10:
		width_note = "\n*(tr_ width not to scale)*"

	await message.channel.send(f"""**<@{message.author.id}>, your generated tr_ is {round(height, 4)}m tall!**
	{width_note}
	{to_scale}""".replace("\t", ""), file=discord.File("Images/generated tr_.png"))

	os.remove("Images/generated tr_.png")

	tr_gen = open("Config/_tr_gen.txt", "r").read().split(" ")
	tr_gen.remove(str(message.id))
	open("Config/_tr_gen.txt", "w").write(" ".join(tr_gen).strip())
	return