import numpy as np

import face_recognition
from scipy import spatial
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

########################################################
def calc_lip_coef(facelandmarks_list):
	'''Calc lip coef
	Если угол между векторами < -0.97, то счастливые или грустные эммоции (True-happy, False-Sad)
	Если > -0,97 то нейтральное

	
	Arguments:
		facelandmarks_list {[type]} -- [description]
	'''
	# Lips handler
	# Make np array
	arr = np.array(facelandmarks_list[0]['top_lip'])
	# Find v_0 and v_1 coordinates
	# Middle point - p_0
	p_0 = arr[8]
	# Angle points p_1 and p_2
	p_1 = arr[0]; p_2 = arr[6]
	# Find vectors 
	vec_0 = p_1 - p_0
	vec_1 = p_2 - p_0
	# Check points on smiling 
	if p_1[1] > p_2[1]:
		smiling_bool = True
	else:
		smiling_bool = False
		
	# Return cos and smiling_bool 
	# if cos < -0.97, it is happy or sad emotion
	return (1 - spatial.distance.cosine(vec_0, vec_1), smiling_bool)

def determ_lips(facelandmarks_list):
	index = calc_lip_coef(facelandmarks_list)

	if index[1] and index[0] > -0.97:
		return 'data/lips/2.png'
	elif not index[1] and index[0] >= -0.97:
		return 'data/lips/0.png'
	else:
		return 'data/lips/1.png'

def calc_nose_coef(facelandmarks_list):
	'''Calc nose coef
	Определяем нос
	
	Arguments:
		facelandmarks_list {[type]} -- [description]
	return:
		(отношение, площядь)
	'''
	# Make np arrays
	bridge_arr = np.array(facelandmarks_list[0]['nose_bridge'])
	tip_arr = np.array(facelandmarks_list[0]['nose_tip'])
	# Find nose hieght
	nose_hieght = tip_arr[np.where(np.min(tip_arr[:,1])==tip_arr[:,1])][0][1] - bridge_arr[0][1]
	# Find nose width 
	nose_width = tip_arr[-1][0] - tip_arr[0][0]
	
	# Return relation of h/w and nose square
	return  (nose_hieght/nose_width, (nose_hieght*nose_width)/2. )

def determ_nose(facelandmarks_list):
	CONST_NOSE_COEF_MEDIUM = 2.0
	CONST_NOSE_COEF_LOW = 1.5

	index = calc_nose_coef(facelandmarks_list)[0]

	if index <= CONST_NOSE_COEF_LOW:
		return 'data/nose/2.png'
	elif CONST_NOSE_COEF_MEDIUM <= index < CONST_NOSE_COEF_LOW:
		return 'data/nose/3.png'
	else:
		return 'data/nose/4.png'

def calc_eyebrow_coef(facelandmarks_list):
	'''Calc eyeborn coef
	Определяет брови
	
	Arguments:
		facelandmarks_list {[type]} -- [description]
	
	Returns:
		{float} -- соотношение длин 
	'''
	# Make np arrays 
	eyebrow_arr = np.array(facelandmarks_list[0]['left_eyebrow'])
	eye_arr = np.array(facelandmarks_list[0]['left_eye'])
	# Find lenght of eyebrow
	eyebrow_len = eyebrow_arr[-1][0] - eyebrow_arr[0][0]
	#print(eyebrow_len)
	# Find lenght of eye
	eye_len = eye_arr[-1][0] - eye_arr[0][0]
	#print(eye_len)
	return eye_len / eyebrow_len

def determ_eyebrow(facelandmarks_list):
	CONST_EYEBROW_COEF_MEDIUM = 1.6
	CONST_EYEBROW_COEF_LOW = 1.4

	index = calc_eyebrow_coef(facelandmarks_list)

	if index <= CONST_EYEBROW_COEF_LOW:
		return 'data/eyebrows/1.png'
	elif CONST_EYEBROW_COEF_MEDIUM <= index < CONST_EYEBROW_COEF_LOW:
		return 'data/eyebrows/2.png'
	else:
		return 'data/eyebrows/3.png'


def calc_eye_coef(facelandmarks_list):
	'''Размер глаз
	
	[description]
	
	Arguments:
		facelandmarks_list {[type]} -- [description]
	
	Returns:
		[type] -- [description]
	'''
	eye_arr = np.array(facelandmarks_list[0]['left_eye'])
	# Find lenght of eye
	eye_len = eye_arr[-1][0] - eye_arr[0][0]
	return eye_len/(eye_arr[4][1] - eye_arr[4][1])

def determ_eye(facelandmarks_list):
	CONST_EYEBROW_COEF_MEDIUM = 1.6
	CONST_EYEBROW_COEF_LOW = 1.4

	index = calc_eye_coef(facelandmarks_list)

	if index <= CONST_EYEBROW_COEF_LOW:
		return 'data/eyes/black_1.png'
	elif CONST_EYEBROW_COEF_MEDIUM <= index < CONST_EYEBROW_COEF_LOW:
		return 'data/eyes/black_2.png'
	else:
		return 'data/eyes/black_3.png'
########################################################
# Генерирует новую картинку
def make_face_shape(type):
	return Image.open(type)

def add_lips(type, image):
	lips = Image.open(type)
	position = ((75), (200))
	image.paste(lips, position, lips)
	return image

def add_eyebrows(type, image):
	eyebrows = Image.open(type)
	position = ((48), (115))
	image.paste(eyebrows, position, eyebrows)
	return image

def add_eyes(type, image):
	eyes = Image.open(type)
	position = ((55), (135))
	image.paste(eyes, position, eyes)
	return image

def add_nose(type, image):
	nose = Image.open(type)
	position = ((93), (135))
	image.paste(nose, position, nose)
	return image

def make_photo(face_shape, lips, eyebrows, eyes, nose, save=False, name='test'):
	print('shape')
	image = make_face_shape(face_shape)
	print('copy')
	image_copy = image.copy()
	print('add_lips')
	image = add_lips(lips, image)
	print('add_eyebrows')
	image = add_eyebrows(eyebrows, image)
	print('add_eyes')
	image = add_eyes(eyes, image)
	print('add_nose')
	image = add_nose(nose, image)
	print('save')
	
	if save:
		# Сохранение
		image.save('data/hand/'+name)
	
	return image

def create_face_shape(pic_path, save=False):
	CONST_CHIN_COEF_MEDIUM = 1.155
	CONST_CHIN_COEF_LOW = 1.10

	index = create_face_mask_choice(create_mask_nake(pic_path, save))

	if index <= CONST_CHIN_COEF_LOW:
		return 'data/faces/small_black.png'
	elif CONST_CHIN_COEF_MEDIUM <= index < CONST_CHIN_COEF_LOW:
		return 'data/faces/medium_black.png'
	else:
		return 'data/faces/large_black.png'

def create_current_mask(pic_path, save=False):
	'''Main func
	
	[description]
	
	Arguments:
		pic_path {[type]} -- [description]
	
	Keyword Arguments:
		save {bool} -- [description] (default: {False})
	'''
	name = pic_path.split('/')[-1].split('.')[0] + '.png'
	origin_img = Image.open(pic_path).convert("RGBA")

	fl = FaceLandmarks()
	fm = FaceMask()

	facelandmarks_list = fl.find_list(pic_path)

	image = make_photo(
			face_shape=create_face_shape(pic_path), 
			lips=determ_lips(facelandmarks_list), 
			eyebrows=determ_eyebrow(facelandmarks_list), 
			eyes=determ_eye(facelandmarks_list), 
			nose=determ_nose(facelandmarks_list), 
			save=False, 
			name=name
			)

	# image = fm.create_mask(FaceLandmarkslist, origin_img)
	if save:
		image.save('data/hand/'+name)

	return 'data/hand/'+name

########################################################
def create_mask_nake(pic_path, save=False):
	name = pic_path.split('/')[-1].split('.')[0] + '.png'
	origin_img = Image.open(pic_path).convert("RGBA")

	fl = FaceLandmarks()
	fm = FaceMask()

	FaceLandmarkslist = fl.find_list(pic_path)

	image = fm.create_mask(FaceLandmarkslist, origin_img)
	if save:
		image.save('data/hand/'+name)
	return FaceLandmarkslist


def create_face_mask_choice(facelandmarks_list):
	# make np array
	arr = np.array(facelandmarks_list[0]['chin'])
	# find max x-coordinate 
	max_x = np.max(arr[:,0])
	# find min x-coordinate
	min_x = np.min(arr[:,0])
	# find max y-coordinate
	max_y = np.max(arr[:,1])
	# find min y-coordinate
	min_y = np.min(arr[:,1])

	return (max_x - min_x) / (max_y - min_y + 10)






if __name__ == '__main__':
	face_shape = '../data/faces/small_black.png'
	lips = '../data/lips/2.png'
	eyebrows = '../data/eyebrows/3.png'
	eyes = '../data/eyes/1.png'
	nose = '../data/nose/2.png' # трубле 3

	make_photo(face_shape, lips, eyebrows, eyes, nose)
