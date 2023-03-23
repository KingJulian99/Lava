from libc.math cimport sqrt 
cimport numpy as np




def liesInBounds(int resolution_y, int resolution_x, int y_center_position, int x_center_position, int y, int x, int space_y_len, int space_x_len):
        if( 0 <= ( (resolution_y - 1) - (y_center_position) - y ) <= (space_y_len - 1) and 0 <= ( (x_center_position) - x) <= (space_x_len - 1)):
            return True
        else:
            return False





def updateGridCircle(self, int resolution_y, int resolution_x, int PARTICLE_RADIUS, float[:, :] space, float[:, :] temperatures):
        
        cdef int y, x, y_position, x_position, height
        cdef float step_x, step_y, width

        step_x = 1.0/resolution_x
        step_y = 1.0/resolution_y
        
        for particle in self.particles:
            y_position = particle.y_coord // step_y
            x_position = particle.x_coord // step_x

            for y in range(-PARTICLE_RADIUS, PARTICLE_RADIUS):
                height = abs(y)

                if(height == 0):
                    width = PARTICLE_RADIUS
                else:
                    width = sqrt(PARTICLE_RADIUS**2 - height**2)

                for x in range(- int (width), int (width)):

                    if(liesInBounds(resolution_y, resolution_x, y_position, x_position, y, x, 100, 100)): 

                        space[int (resolution_y - 1) - int (y_position) - y][int (x_position) - x] = 1.0
                        temperatures[int (resolution_y - 1) - int (y_position) - y][int (x_position) - x] += (2.0 - min(1.0, (self.getNormalizedDistance(x, y, 0, 0, PARTICLE_RADIUS))) * 2.0)