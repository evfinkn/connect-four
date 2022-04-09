### To-do list
- [ ] Make resizable window
- [x] Fix warning messages
  - [x] Warning when writing file after closing window
  - [x] Warning when game is won
- [ ] Finish README.md
- [ ] Make screen 1 slot_size taller (so window is square)
- [ ] Fix win_screen
  - [ ] Show "Color wins!" in new extra space at top
  - [ ] Move new game button to top as well ?
- [x] Make find_win return a dictionary
- [ ] Instead of redrawing board every frame, make a board surface and blit it every frame, only updating that surface when a new coin is played
- [ ] Similar to above, but for the board after being won and winscreen
- [ ] Define a nested function in find_win that does the operations of the return statements on an input
- [ ] Change (width + extra_space * 2) // 2 to width // 2 + extra_space, same with height
- [ ] Make extra_space independent of slot_size
- [ ] Stop game if board is full and there is no win