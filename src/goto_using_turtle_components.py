    
    def goto(self, x, y=None):
        """ mimic turtle rtu without explicit goto call
        because explicit goto appears to mess up tkinter
        coordinates
        """
        self.goto_pre(x,y)
        old_heading = self.rtu.heading()
        cur_x, cur_y = self.rtu.position()
        angle = self.rtu.towards(x=x, y=y)
        distance = self.rtu.distance(x=x, y=y)
        new_heading = old_heading+angle
        self.setheading(new_heading)
        self.rtu.forward(distance)
        self.rtu.setheading(old_heading)
        
        self.goto_post(x,y) 
