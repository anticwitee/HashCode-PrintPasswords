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
        # diff1 = len(self.tags.difference(slide.tags))
        diff1 = abs(len(self.tags) - union)
        diff2 = abs(len(self.tags) - diff1)
        return min(union, diff1, diff2)

    def __str__(self):
        return f"{self.pics} {self.tags}"

if len(sys.argv) != 3:
    print("provide in && out relative paths")
    sys.exit()

in_fname = sys.argv[1]
out_fname = sys.argv[2]

photos = {}
with open(in_fname) as f:
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

current_milli_time = lambda: int(round(time.time() * 1000))

for v_pic_num1 in vert_pics:
    min_int = -1
    best_pic_num = -1
    if vert_pics[v_pic_num1] == None:
        continue
    first_set = set(vert_pics[v_pic_num1][2:])
    t1 = current_milli_time()
    for v_pic_num2 in vert_pics:
        if v_pic_num1 == v_pic_num2 or vert_pics[v_pic_num2] == None:
            continue
        if current_milli_time() - t1 > 2 and best_pic_num > -1:
            break
        second_set = set(vert_pics[v_pic_num2][2:])
        intersect = len(first_set.intersection(second_set))
        if intersect > min_int:
            min_int = intersect
            best_pic_num = v_pic_num2
    slides.add(Slide(
        (v_pic_num1, best_pic_num),
        first_set.union(set(vert_pics[best_pic_num][2:]))
    ))
    if last_slide == None:
        last_slide = slide
    vert_pics[v_pic_num1] = None
    vert_pics[best_pic_num] = None


with open(out_fname, 'w') as out:
    n = len(slides) + 1
    out.write(f"{n}\n")

    if len(last_slide.pics) == 2:
        out.write(f"{last_slide.pics[0]} {last_slide.pics[1]}\n")
    else:
        out.write(f"{last_slide.pics[0]}\n")

    while len(slides) > 0:
        best_slide = None
        best_interest = -1
        t1 = current_milli_time()
        for slide in slides:
            if current_milli_time() - t1 > 5 and best_slide != None:
                break
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
