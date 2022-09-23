# Simple pygame program
# Import and initialize the pygame library
import pygame
import math
clock = pygame.time.Clock()
pygame.init()

class Planet:
  
  planets_list = []
  
  def __init__(self):
    self.__class__.planets_list.append(self)
    self.x_pos = 250
    self.y_pos = 250
    self.x_vel = 0
    self.y_vel = 0
    self.mass = 100
    self.diameter = 1
    self.force = 0
    self.fixed = False
    pygame.draw.circle(screen, (0, 0, 255), (int(self.x_pos), int(self.y_pos)), self.diameter)
  
  def change_coords(self, x, y):
    self.x_pos = x
    self.y_pos = y
    screen.fill((255, 255, 255))
    for planet in self.planets_list:
      pygame.draw.circle(screen, (0, 0, 0), (int(planet.x_pos), int(planet.y_pos)), planet.diameter)


class PhysicsEngine:
  
  @staticmethod
  def calculate_gravity():
    for planet in Planet.planets_list:
      # initialize vector components to zero so that all forces on a planet can be summed
      vector_x = 0
      vector_y = 0
      for secondary_planet in Planet.planets_list:
        if planet == secondary_planet:
          continue
        elif planet.fixed == True:
          continue
        # calculates distance of secondary_planet from planet
        distance = PhysicsEngine.calculate_distance(planet.x_pos, planet.y_pos, secondary_planet.x_pos, secondary_planet.y_pos)
        # calculates the angle of secondary_planet from planet
        angle = PhysicsEngine.calculate_angle(planet.x_pos, planet.y_pos, secondary_planet.x_pos, secondary_planet.y_pos)
        # calculates the force on planet based on Newton's second law of motion
        planet.force = .4*((planet.mass * secondary_planet.mass) / (distance**2))
        # convert force and angle into vector component form ex: (x force, y force)
        vector_x += planet.force * (math.cos(math.radians(angle)))
        vector_y += planet.force * (math.sin(math.radians(angle)))
      # calculate acceleration and add it to planet's velocity using a = f/m  (f = ma)
      planet.x_vel += vector_x/planet.mass
      planet.y_vel += vector_y/planet.mass
      # adding the current velocity to the planet's position
      planet.x_pos += planet.x_vel
      planet.y_pos += planet.y_vel
      # update visual position of planets
      planet.change_coords(planet.x_pos, planet.y_pos)

  @staticmethod
  def calculate_collisions():
    for planet in Planet.planets_list:
      for secondary_planet in Planet.planets_list:
        if planet == secondary_planet:
          continue
        elif planet.fixed == True:
          continue
        elif PhysicsEngine.calculate_distance(planet.x_pos, planet.y_pos, secondary_planet.x_pos, secondary_planet.y_pos) < (planet.diameter + secondary_planet.diameter):
          # physics for colliding objects go here
          planet.x_vel = 0
          planet.y_vel = 0
          secondary_planet.x_vel = 0
          secondary_planet.y_vel = 0
  
  # finally got frustrated with this function and discovered atan2() as opposed to atan() and determining quadrants
  @staticmethod
  def calculate_angle(x1, y1, x2, y2):
    y = (y2 - y1)
    x = (x2 - x1)
    if math.degrees(math.atan2(y, x)) > 0:
      return math.degrees(math.atan2(y, x))
    elif math.degrees(math.atan2(y, x)) < 0:
      return math.degrees(math.atan2(y, x)) + 360
    else:
      return 0
  
  @staticmethod
  def calculate_distance(x1, y1, x2, y2):
    return math.sqrt( (x2 - x1)**2 + (y2 - y1)**2 )
    
    

# Set up the drawing window
screen = pygame.display.set_mode([1000, 1000], pygame.FULLSCREEN)
dt = clock.tick(60)

# planet initialization and starting configs
earth = Planet()
earth.mass = 10000
earth.diameter = 15
moon = Planet()
moon.y_vel = -1
moon.x_vel = 3
moon.mass = 80
moon.diameter = 5
sun = Planet()
sun.y_vel = -1.3
sun.x_vel = 3.6
sun.mass = 4
mars = Planet()
mars.mass = 250
mars.diameter = 10
mars.y_vel = -4
mars.change_coords(800, 800)
sun.change_coords(275, 175)
earth.change_coords(600, 500)
moon.change_coords(300, 200)

# game loop
running = True
while running:
    # Did the user click the window close button?
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fill the background with white
    screen.fill((255, 255, 255))

    PhysicsEngine.calculate_collisions()
    PhysicsEngine.calculate_gravity()

    # makes it easier to watch the planets move
    pygame.time.delay(20)
    
    # Flip the display
    pygame.display.flip()

# Done! Time to quit.
pygame.quit()