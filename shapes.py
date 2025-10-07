import cv2
import numpy as np

def draw_shapes(frame, shapes_drawn):
    """Draw all stored shapes on frame"""
    for shape in shapes_drawn:
        t = shape['type']
        if t in ['Triangle','Rectangle','Square','Pentagon','Hexagon']:
            cv2.drawContours(frame, [shape['approx']], -1, (0,255,255), 3)
        elif t=='Circle/Ellipse':
            cv2.circle(frame, shape['center'], shape['radius'], (0,255,255), 3)
        elif t=='Text':
            font_scale = shape.get('font_scale', 1.0)
            pos = shape['pos']
            cv2.putText(frame, shape['text'], pos, cv2.FONT_HERSHEY_SIMPLEX,
                        font_scale, (0,0,255), 2)
    return frame

def detect_shape(points):
    """Detect rough shape and return structured info"""
    pts = np.array(points, np.int32)
    hull = cv2.convexHull(pts)
    approx = cv2.approxPolyDP(hull, 0.04*cv2.arcLength(hull, True), True)
    vertices = len(approx)
    shape_info = {'type': 'Unidentified', 'pos': (50,50)}

    if vertices==3:
        shape_info['type']='Triangle'; shape_info['approx']=approx
    elif vertices==4:
        shape_info['type']='Rectangle'; shape_info['approx']=approx
    elif vertices==5:
        shape_info['type']='Pentagon'; shape_info['approx']=approx
    elif vertices==6:
        shape_info['type']='Hexagon'; shape_info['approx']=approx
    else:
        (x_c, y_c), radius = cv2.minEnclosingCircle(hull)
        shape_info['type']='Circle/Ellipse'
        shape_info['center']=(int(x_c), int(y_c)); shape_info['radius']=int(radius)

    return shape_info

def select_shape(pos, shapes_drawn):
    """Return the shape under given point, if any"""
    x, y = pos
    for shape in reversed(shapes_drawn):  # top-most first
        t = shape['type']
        if t in ['Triangle','Rectangle','Square','Pentagon','Hexagon']:
            pts = shape['approx'].reshape(-1,2)
            if cv2.pointPolygonTest(pts, pos, False) >= 0:
                return shape
        elif t=='Circle/Ellipse':
            c = shape['center']; r = shape['radius']
            if np.hypot(x - c[0], y - c[1]) <= r:
                return shape
    return None

def reshape_shape(shape, scale):
    """Scale the shape around its center"""
    if shape['type'] in ['Triangle','Rectangle','Square','Pentagon','Hexagon']:
        pts = shape['approx'].reshape(-1,2)
        center = np.mean(pts, axis=0)
        pts = ((pts - center) * scale + center).astype(np.int32)
        shape['approx'] = pts.reshape(-1,1,2)
    elif shape['type']=='Circle/Ellipse':
        shape['radius'] = max(10,int(shape['radius']*scale))

def move_shape(shape, new_center):
    """Move shape to new_center"""
    if shape['type'] in ['Triangle','Rectangle','Square','Pentagon','Hexagon']:
        pts = shape['approx'].reshape(-1,2)
        center = np.mean(pts, axis=0)
        delta = np.array(new_center) - center
        pts = (pts + delta).astype(np.int32)
        shape['approx'] = pts.reshape(-1,1,2)
    elif shape['type']=='Circle/Ellipse':
        shape['center'] = new_center
