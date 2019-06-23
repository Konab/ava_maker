import face_recognition
from PIL import Image, ImageFont, ImageDraw


class FaceLandmarks(object):

    def __init__(self):
        pass

    def find_list(self, name_file):
        image = face_recognition.load_image_file(name_file) 
        return face_recognition.face_landmarks(image)

    def find_box(self, name_file):
        image = face_recognition.load_image_file(name_file) 
        return face_recognition.face_locations(image)


class FaceMask(object):

    def __init__(self):
        pass

    def create_mask(self, face_landmarks_list, origin_img):

        shape_img = Image.new("RGBA", origin_img.size, color=(255, 255, 255, 0))
        shape_draw = ImageDraw.Draw(shape_img)
        #for i in range(len(triangles_list)-1):
           # shape_draw.line((triangles_list[i], triangles_list[i+1]), fill=(0,0,0), width=4)

        # Draw line of Faces Landmark
        for i in face_landmarks_list[0]:
            for j in range( len(face_landmarks_list[0][i]) - 1 ):
                shape_draw.point(face_landmarks_list[0][i][j],fill=50)
                shape_draw.line((face_landmarks_list[0][i][j], face_landmarks_list[0][i][j+1]), fill=(0,0,0), width=4)
        
        shape_draw.line((face_landmarks_list[0]['right_eye'][0], face_landmarks_list[0]['right_eye'][-1]), fill=(0,0,0), width=4)
        shape_draw.line((face_landmarks_list[0]['left_eye'][0], face_landmarks_list[0]['left_eye'][-1]), fill=(0,0,0), width=4)


        return shape_img


def create_mask_(pic_path, save=False):
	name = pic_path.split('/')[-1].split('.')[0] + '.png'
	origin_img = Image.open(pic_path).convert("RGBA")

	fl = FaceLandmarks()
	fm = FaceMask()

	FaceLandmarkslist = fl.find_list(pic_path)

	image = fm.create_mask(FaceLandmarkslist, origin_img)
	if save:
		image.save('data/hand/'+name)
	return 
