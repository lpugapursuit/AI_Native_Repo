# Animated Chess Game with Intelligent AI

A beautiful, feature-rich chess game with animated graphics, custom piece designs, full playability, and an intelligent AI opponent built with HTML5, CSS3, and JavaScript.

## Features

### 🎮 Game Features
- **Full Chess Rules**: Complete implementation of all chess piece movements and rules
- **Intelligent AI Opponent**: Advanced chess AI with 4 difficulty levels (Easy, Medium, Hard, Expert)
- **Animated Graphics**: Smooth piece movement animations with rotation effects
- **Custom Piece Designs**: Beautiful Unicode chess pieces with gradient styling
- **Move Validation**: Real-time validation of all chess moves
- **Pawn Promotion**: Automatic promotion modal when pawns reach the end
- **Game Statistics**: Move counter, capture counter, and game timer
- **Move History**: Complete history of all moves made in the game
- **Captured Pieces Display**: Visual display of all captured pieces

### 🤖 AI Features
- **Minimax Algorithm**: Advanced search algorithm with alpha-beta pruning
- **Position Evaluation**: Comprehensive board evaluation with piece-square tables
- **Tactical Awareness**: Detects captures, checks, forks, pins, and discovered attacks
- **Strategic Play**: Understands opening principles, center control, and king safety
- **Adaptive Difficulty**: 
  - **Easy**: 30% randomness, depth 2, ~1s thinking time
  - **Medium**: 10% randomness, depth 3, ~2s thinking time
  - **Hard**: 5% randomness, depth 4, ~3s thinking time
  - **Expert**: 1% randomness, depth 5, ~5s thinking time
- **Game Modes**: Player vs Player, Player vs Computer, Computer vs Computer

### 🎨 Visual Features
- **Modern UI**: Glassmorphism design with backdrop blur effects
- **Responsive Design**: Works on desktop, tablet, and mobile devices
- **Interactive Highlights**: Visual feedback for selected pieces and valid moves
- **Sound Effects**: Optional move sound effects using Web Audio API
- **Victory Animations**: Special animations for game end states
- **Coordinate Labels**: File and rank labels for easy board navigation
- **Computer Thinking Animation**: Visual indicator when AI is calculating moves

### 🎯 Game Controls
- **New Game**: Start a fresh game with mode selection (PvP or PvC)
- **Undo Move**: Go back one move (undoes both player and computer moves in PvC)
- **Flip Board**: Rotate the board perspective
- **Sound Toggle**: Enable/disable move sound effects
- **Mode Switching**: Switch between Player vs Player and Player vs Computer
- **Computer vs Computer**: Watch two AI engines play against each other

## How to Play

### Standalone Version
1. Open `chess_ultimate.html` in any modern web browser
2. Choose your game mode: Player vs Player or Player vs Computer
3. If playing against computer, select difficulty level
4. Click on a piece to select it
5. Click on a valid square to move the piece
6. When a pawn reaches the opposite end, choose a promotion piece
7. Play until checkmate or stalemate

### AI Difficulty Levels
- **Easy**: Perfect for beginners. AI makes occasional mistakes and focuses on basic strategies
- **Medium**: Balanced gameplay for intermediate players. Good mix of strategy and accessibility
- **Hard**: Challenging for experienced players. AI uses advanced tactics and looks several moves ahead
- **Expert**: For the most skilled players. Deep analysis with complex positional understanding

## File Structure

```
├── chess_ultimate.html     # Complete chess game with intelligent AI
├── chess_standalone.html   # Basic chess game (no AI)
├── chess_app.py           # Flask backend with game logic
├── templates/
│   └── chess.html         # Flask template version
├── requirements.txt        # Python dependencies
└── README.md              # This file
```

## Technical Details

### Frontend Technologies
- **HTML5**: Semantic structure and accessibility
- **CSS3**: Modern styling with gradients, animations, and responsive design
- **JavaScript ES6+**: Object-oriented game logic with classes
- **Web Audio API**: Sound effects for move feedback

### AI Engine Technologies
- **Minimax Algorithm**: Recursive search for optimal moves
- **Alpha-Beta Pruning**: Dramatically improves search efficiency
- **Position Evaluation**: Piece values, positional bonuses, mobility, pawn structure
- **Tactical Detection**: Captures, checks, forks, pins, discovered attacks
- **Move Ordering**: Prioritizes promising moves for better pruning

### Backend Technologies (Flask Version)
- **Flask**: Python web framework
- **Flask-SocketIO**: Real-time communication for multiplayer
- **Python**: Game logic and move validation

### Key Features Implementation
- **Move Validation**: Complete chess rule implementation for all pieces
- **Animation System**: CSS animations with JavaScript timing control
- **State Management**: Comprehensive game state tracking
- **Responsive Design**: Mobile-first approach with flexible layouts
- **AI Engine**: Intelligent move selection with difficulty-based behavior

## Browser Compatibility

- Chrome 60+
- Firefox 55+
- Safari 12+
- Edge 79+

## Future Enhancements

- [x] AI opponent with different difficulty levels ✅ **COMPLETED**
- [ ] Multiplayer support via WebSockets
- [ ] Game save/load functionality
- [ ] Advanced move analysis
- [ ] Tournament mode
- [ ] Custom board themes
- [ ] Move notation (algebraic notation)
- [ ] Opening book integration
- [ ] Endgame tablebase integration

## Contributing

Feel free to contribute to this project by:
- Adding new features
- Improving the AI engine
- Enhancing the UI/UX
- Fixing bugs
- Adding tests
- Improving documentation

## License

This project is open source and available under the MIT License.

---

**Enjoy playing chess against our intelligent AI! ♔♛🤖**