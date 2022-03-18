# pygame_chase_demo
A game where an input (mouse/ motion input) can chase an object around a screen (or projected image)

# Why does this exist
A local Target store near me has a projection mapped pong game on the floor.

![image](https://user-images.githubusercontent.com/22123843/159080329-49c4dc78-5b54-4230-b4b0-06cd149e47ff.png)

That got me thinking I should try to build something similar that my pets could chase on the floor. (2 dogs, 1 cat)

What I have done so far with pygame is build a small game where a Predator (currently mouse input) can chase Prey around a screen.

![image](https://user-images.githubusercontent.com/22123843/159080825-291f55c4-4a99-428c-b050-b94f0accd8a6.png)

The blue circle is controlled by mouse input and as it moves closer to the red circle, the red circle flees.
As the red cicle crosses outside of the inner grey boundry, it begins to rotate around so it doesnt get stuck in a corner.

There are some simple variables controlling resolution, usable space, and how quickly the prey will flee.

![image](https://user-images.githubusercontent.com/22123843/159081162-da5767d2-d9d8-4dbe-99ef-44eee31af1d4.png)

# What's next
If I ever get a large chunk of free time with zero obligation (and a projector, I don't have that either) I'd like to set up a motion tracking based input so my pets, a hand, or really anything, could break the boundry of the rectangle and track its location, so the prey would flee from that.  There are lots of demos online of using projection mapping & motion tracking to create an input within a projected plane. This would be another way that can be used.





