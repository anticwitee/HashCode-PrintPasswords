import sys
import time

class Slide:
    # tags are sets
    # pics are tuple
    def __init__(self,pics,tags):
        self.pics = pics
        self.tags = tags
        
    def interest_factor(self, slide):
        union = len(self.tags.intersection(slide.tags))
        diff1 = len(self.tags.difference(slide.tags))
        diff2 = abs(len(self.tags) - diff1)
        return min(union, diff1, diff2)

    def __str__(self):
        return f"{self.pics} {self.tags}"

filename = sys.argv[1]
photos = {}
with open(filename) as f:
    num_photos = f.readline()
    for i, line in enumerate(f):
        # format = ORIENTATION TAG_NUMBER <TAGS>
        photo = tuple(line.strip().split())
        photos[i] = photo

slides = set()
last_slide = None
vert_pics = {}
for photo_num in photos:
    photo = photos[photo_num]
    if photo[0] == 'H':
        slide = Slide((photo_num,), set(photo[2:]))
        if last_slide == None:
            last_slide = slide
        else:
            slides.add(slide)
    else:
        vert_pics[photo_num] = photo
        if vert_pic == None:
            vert_pic = (photo_num,photo)
        else:
            slide = Slide(
                (photo_num,vert_pic[0]), 
                set(vert_pic[1][2:]).union(set(photo[2:]))
            )
            if last_slide == None:
                last_slide = slide
            else:
                slides.add(slide)
            vert_pic = None


with open(f'out/{filename}', 'w') as out:
    n = len(slides) + 1
    out.write(f"{n}\n")

    if len(last_slide.pics) == 2:
        out.write(f"{last_slide.pics[0]} {last_slide.pics[1]}\n")
    else:
        out.write(f"{last_slide.pics[0]}\n")

    while len(slides) > 0:
        best_slide = None
        best_interest = -1
        for slide in slides:
            new_interest = last_slide.interest_factor(slide)
            if new_interest > best_interest:
                best_slide = slide
                best_interest = new_interest
        if len(best_slide.pics) == 2:
            out.write(f"{best_slide.pics[0]} {best_slide.pics[1]}\n")
        else:
            out.write(f"{best_slide.pics[0]}\n")
        slides.remove(best_slide)
        last_slide = best_slide
