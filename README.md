# Animated Chess Game

A beautiful, feature-rich chess game with animated graphics, custom piece designs, and full playability built with HTML5, CSS3, and JavaScript.

## Features

### 🎮 Game Features
- **Full Chess Rules**: Complete implementation of all chess piece movements and rules
- **Animated Graphics**: Smooth piece movement animations with rotation effects
- **Custom Piece Designs**: Beautiful Unicode chess pieces with gradient styling
- **Move Validation**: Real-time validation of all chess moves
- **Pawn Promotion**: Automatic promotion modal when pawns reach the end
- **Game Statistics**: Move counter, capture counter, and game timer
- **Move History**: Complete history of all moves made in the game
- **Captured Pieces Display**: Visual display of all captured pieces

### 🎨 Visual Features
- **Modern UI**: Glassmorphism design with backdrop blur effects
- **Responsive Design**: Works on desktop, tablet, and mobile devices
- **Interactive Highlights**: Visual feedback for selected pieces and valid moves
- **Sound Effects**: Optional move sound effects using Web Audio API
- **Victory Animations**: Special animations for game end states
- **Coordinate Labels**: File and rank labels for easy board navigation

### 🎯 Game Controls
- **New Game**: Start a fresh game at any time
- **Undo Move**: Go back one move (basic implementation)
- **Flip Board**: Rotate the board perspective
- **Sound Toggle**: Enable/disable move sound effects

## How to Play

### Standalone Version
1. Open `chess_standalone.html` in any modern web browser
2. Click on a piece to select it
3. Click on a valid square to move the piece
4. When a pawn reaches the opposite end, choose a promotion piece
5. Play until checkmate or stalemate

### Flask Backend Version
1. Install dependencies: `pip install -r requirements.txt`
2. Run the Flask server: `python chess_app.py`
3. Open your browser to `http://localhost:5000`
4. Play chess with full backend support and potential multiplayer features

## File Structure

```
├── chess_standalone.html    # Standalone chess game (no server needed)
├── chess_app.py            # Flask backend with game logic
├── templates/
│   └── chess.html          # Flask template version
├── requirements.txt         # Python dependencies
└── README.md               # This file
```

## Technical Details

### Frontend Technologies
- **HTML5**: Semantic structure and accessibility
- **CSS3**: Modern styling with gradients, animations, and responsive design
- **JavaScript ES6+**: Object-oriented game logic with classes
- **Web Audio API**: Sound effects for move feedback

### Backend Technologies (Flask Version)
- **Flask**: Python web framework
- **Flask-SocketIO**: Real-time communication for multiplayer
- **Python**: Game logic and move validation

### Key Features Implementation
- **Move Validation**: Complete chess rule implementation for all pieces
- **Animation System**: CSS animations with JavaScript timing control
- **State Management**: Comprehensive game state tracking
- **Responsive Design**: Mobile-first approach with flexible layouts

## Browser Compatibility

- Chrome 60+
- Firefox 55+
- Safari 12+
- Edge 79+

## Future Enhancements

- [ ] Multiplayer support via WebSockets
- [ ] AI opponent with different difficulty levels
- [ ] Game save/load functionality
- [ ] Advanced move analysis
- [ ] Tournament mode
- [ ] Custom board themes
- [ ] Move notation (algebraic notation)
- [ ] Opening book integration

## Contributing

Feel free to contribute to this project by:
- Adding new features
- Improving the UI/UX
- Fixing bugs
- Adding tests
- Improving documentation

## License

This project is open source and available under the MIT License.

---

**Enjoy playing chess! ♔♛**