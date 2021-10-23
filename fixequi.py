import moderngl
import numpy as np
import math
import sys
from PIL import Image


start_image = Image.open(sys.argv[1])
start_width, start_height = start_image.size
crop_width = start_width / 2;

left_image = start_image.crop((0,0, crop_width , start_height))
right_image = start_image.crop((crop_width, 0, start_width , start_height))

ctx = moderngl.create_standalone_context()

input_texture = ctx.texture(right_image.size, 3, right_image.tobytes())
sampler = ctx.sampler(texture=input_texture) 

prog = ctx.program(
    vertex_shader='''
        #version 330

        in vec2 in_vert;
        in vec2 in_uv;
         
        out vec2 f_uv; 

        void main() {
            
            f_uv = in_uv; 
            gl_Position = vec4(in_vert , 0.0, 1.0);


        }
    ''',
    fragment_shader='''
        #version 330
        #define PI 3.1415926538

        uniform sampler2D Texture;
        uniform vec3 in_corrections;

        in vec2 f_uv;
 
        out vec4 f_color;

        void main() {
            
            vec3 sin_theta = sin(in_corrections);
            vec3 cos_theta = cos(in_corrections);

            mat3 rotx = mat3(
                   1.0, 0.0 , 0.0,
                   0.0, cos_theta.x , -sin_theta.x,
                   0.0, sin_theta.x, cos_theta.x);

            mat3 roty = mat3(
                   cos_theta.y , 0.0, sin_theta.y,
                   0.0, 1.0 , 0.0,
                   -sin_theta.y, 0, cos_theta.y);

            mat3 rotz = mat3(
                   cos_theta.z, -sin_theta.z, 0.0,
                   sin_theta.z,  cos_theta.z, 0.0,
                   0.0,          0.0,         1.0);

            mat3 rot_m = rotx * roty * rotz;

            vec2 rot_uv = f_uv * vec2(PI, PI);
             
            vec2 sin_rot_uv = sin(rot_uv);
            vec2 cos_rot_uv = cos(rot_uv);

            vec3 cart = vec3(-sin_rot_uv.y * cos_rot_uv.x,
                              sin_rot_uv.y * sin_rot_uv.x,
                              cos_rot_uv.y);

            vec3 cart_rot = cart * rot_m;
            
            vec2 final_uv = vec2(atan(cart_rot.y, -cart_rot.x), acos(cart_rot.z)); 
            if(final_uv.x < 0) {
               final_uv.x += (PI * 2.0);   
            }

            final_uv /= PI ; 
            f_color = texture(Texture, final_uv);
//            f_color = vec4(final_uv.x, final_uv.y , 0.0, 1.0 );
        }
    ''',
)

in_corrections = prog['in_corrections'];
in_corrections.value = (math.radians(2.0), 0.0, 0.0);

vertices = np.array([
                1.0, 1.0,             1.0, 0.0, 
                -1.0, 1.0,            0.0, 0.0, 
                1.0, -1.0,            1.0, 1.0, 
                -1.0, -1.0,           0.0, 1.0, 
                -1.0, 1.0,            0.0, 0.0, 
                1.0, -1.0,            1.0, 1.0, 
])

vbo = ctx.buffer(vertices.astype('f4').tobytes())
vao = ctx.simple_vertex_array(prog, vbo, 'in_vert', 'in_uv')

fbo = ctx.simple_framebuffer((2160,2160))
fbo.use()
fbo.clear(0.0, 1.0, 0.0, 1.0)

vao.scope = ctx.scope(framebuffer=fbo, samplers=[
            sampler.assign(0),
])



vao.render(moderngl.TRIANGLES)

fixed_image = Image.frombytes('RGB', fbo.size, fbo.read(), 'raw', 'RGB', 0, -1)
start_image.paste(fixed_image, (int(crop_width), 0));
start_image.save(sys.argv[2])

