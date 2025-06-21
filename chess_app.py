from flask import Flask, render_template, request, jsonify, session
from flask_socketio import SocketIO, emit, join_room, leave_room
import json
import uuid
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'
socketio = SocketIO(app, cors_allowed_origins="*")

# Store active games
games = {}

class ChessGame:
    def __init__(self, game_id):
        self.game_id = game_id
        self.board = self.initialize_board()
        self.current_player = 'white'
        self.move_history = []
        self.game_over = False
        self.players = {'white': None, 'black': None}
        self.created_at = datetime.now()
        
    def initialize_board(self):
        return [
            ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r'],
            ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'],
            ['', '', '', '', '', '', '', ''],
            ['', '', '', '', '', '', '', ''],
            ['', '', '', '', '', '', '', ''],
            ['', '', '', '', '', '', '', ''],
            ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
            ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R']
        ]
    
    def make_move(self, from_row, from_col, to_row, to_col, promotion_piece=None):
        piece = self.board[from_row][from_col]
        if not piece:
            return False, "No piece at source position"
            
        # Validate move
        if not self.is_valid_move(from_row, from_col, to_row, to_col):
            return False, "Invalid move"
            
        # Execute move
        target_piece = self.board[to_row][to_col]
        self.board[from_row][from_col] = ''
        
        if promotion_piece and piece.lower() == 'p' and (to_row == 0 or to_row == 7):
            self.board[to_row][to_col] = promotion_piece
        else:
            self.board[to_row][to_col] = piece
            
        # Record move
        move_data = {
            'from': [from_row, from_col],
            'to': [to_row, to_col],
            'piece': piece,
            'captured': target_piece,
            'promotion': promotion_piece,
            'timestamp': datetime.now().isoformat()
        }
        self.move_history.append(move_data)
        
        # Switch players
        self.current_player = 'black' if self.current_player == 'white' else 'white'
        
        # Check game end conditions
        self.check_game_end()
        
        return True, "Move successful"
    
    def is_valid_move(self, from_row, from_col, to_row, to_col):
        piece = self.board[from_row][from_col]
        if not piece:
            return False
            
        # Basic validation - piece belongs to current player
        is_white_piece = piece == piece.upper()
        if (self.current_player == 'white' and not is_white_piece) or \
           (self.current_player == 'black' and is_white_piece):
            return False
            
        # Check if target is own piece
        target_piece = self.board[to_row][to_col]
        if target_piece:
            is_target_white = target_piece == target_piece.upper()
            if is_white_piece == is_target_white:
                return False
                
        # Piece-specific validation
        piece_type = piece.lower()
        if piece_type == 'p':
            return self.is_valid_pawn_move(from_row, from_col, to_row, to_col)
        elif piece_type == 'r':
            return self.is_valid_rook_move(from_row, from_col, to_row, to_col)
        elif piece_type == 'n':
            return self.is_valid_knight_move(from_row, from_col, to_row, to_col)
        elif piece_type == 'b':
            return self.is_valid_bishop_move(from_row, from_col, to_row, to_col)
        elif piece_type == 'q':
            return self.is_valid_queen_move(from_row, from_col, to_row, to_col)
        elif piece_type == 'k':
            return self.is_valid_king_move(from_row, from_col, to_row, to_col)
            
        return False
    
    def is_valid_pawn_move(self, from_row, from_col, to_row, to_col):
        piece = self.board[from_row][from_col]
        is_white = piece == 'P'
        direction = -1 if is_white else 1
        start_row = 6 if is_white else 1
        
        row_diff = to_row - from_row
        col_diff = abs(to_col - from_col)
        target_piece = self.board[to_row][to_col]
        
        # Forward move
        if col_diff == 0 and not target_piece:
            if row_diff == direction:
                return True
            if from_row == start_row and row_diff == 2 * direction:
                return not self.board[from_row + direction][from_col]
        
        # Capture move
        if col_diff == 1 and row_diff == direction and target_piece:
            return True
            
        return False
    
    def is_valid_rook_move(self, from_row, from_col, to_row, to_col):
        if from_row != to_row and from_col != to_col:
            return False
        return self.is_path_clear(from_row, from_col, to_row, to_col)
    
    def is_valid_knight_move(self, from_row, from_col, to_row, to_col):
        row_diff = abs(to_row - from_row)
        col_diff = abs(to_col - from_col)
        return (row_diff == 2 and col_diff == 1) or (row_diff == 1 and col_diff == 2)
    
    def is_valid_bishop_move(self, from_row, from_col, to_row, to_col):
        if abs(to_row - from_row) != abs(to_col - from_col):
            return False
        return self.is_path_clear(from_row, from_col, to_row, to_col)
    
    def is_valid_queen_move(self, from_row, from_col, to_row, to_col):
        return self.is_valid_rook_move(from_row, from_col, to_row, to_col) or \
               self.is_valid_bishop_move(from_row, from_col, to_row, to_col)
    
    def is_valid_king_move(self, from_row, from_col, to_row, to_col):
        row_diff = abs(to_row - from_row)
        col_diff = abs(to_col - from_col)
        return row_diff <= 1 and col_diff <= 1
    
    def is_path_clear(self, from_row, from_col, to_row, to_col):
        row_step = 0 if from_row == to_row else (to_row - from_row) // abs(to_row - from_row)
        col_step = 0 if from_col == to_col else (to_col - from_col) // abs(to_col - from_col)
        
        current_row = from_row + row_step
        current_col = from_col + col_step
        
        while current_row != to_row or current_col != to_col:
            if self.board[current_row][current_col]:
                return False
            current_row += row_step
            current_col += col_step
            
        return True
    
    def check_game_end(self):
        # Basic implementation - could be enhanced with proper checkmate detection
        if not self.has_valid_moves():
            self.game_over = True
    
    def has_valid_moves(self):
        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                if piece:
                    is_white_piece = piece == piece.upper()
                    if ((self.current_player == 'white' and is_white_piece) or
                        (self.current_player == 'black' and not is_white_piece)):
                        for to_row in range(8):
                            for to_col in range(8):
                                if self.is_valid_move(row, col, to_row, to_col):
                                    return True
        return False
    
    def get_game_state(self):
        return {
            'board': self.board,
            'current_player': self.current_player,
            'move_history': self.move_history,
            'game_over': self.game_over,
            'players': self.players
        }

@app.route('/')
def home():
    return render_template('chess.html')

@app.route('/api/games', methods=['GET'])
def get_games():
    game_list = []
    for game_id, game in games.items():
        game_list.append({
            'id': game_id,
            'players': game.players,
            'created_at': game.created_at.isoformat(),
            'game_over': game.game_over
        })
    return jsonify(game_list)

@app.route('/api/games', methods=['POST'])
def create_game():
    game_id = str(uuid.uuid4())
    games[game_id] = ChessGame(game_id)
    return jsonify({'game_id': game_id})

@app.route('/api/games/<game_id>', methods=['GET'])
def get_game(game_id):
    if game_id not in games:
        return jsonify({'error': 'Game not found'}), 404
    return jsonify(games[game_id].get_game_state())

@app.route('/api/games/<game_id>/move', methods=['POST'])
def make_move(game_id):
    if game_id not in games:
        return jsonify({'error': 'Game not found'}), 404
        
    data = request.get_json()
    from_row = data.get('from_row')
    from_col = data.get('from_col')
    to_row = data.get('to_row')
    to_col = data.get('to_col')
    promotion_piece = data.get('promotion_piece')
    
    game = games[game_id]
    success, message = game.make_move(from_row, from_col, to_row, to_col, promotion_piece)
    
    if success:
        # Emit move to all players in the game room
        socketio.emit('move_made', {
            'from': [from_row, from_col],
            'to': [to_row, to_col],
            'piece': game.board[to_row][to_col],
            'current_player': game.current_player,
            'game_over': game.game_over
        }, room=game_id)
        
        return jsonify({'success': True, 'message': message})
    else:
        return jsonify({'success': False, 'message': message}), 400

@socketio.on('join_game')
def on_join_game(data):
    game_id = data['game_id']
    player_color = data['color']
    
    if game_id in games:
        game = games[game_id]
        if game.players[player_color] is None:
            game.players[player_color] = request.sid
            join_room(game_id)
            emit('player_joined', {
                'color': player_color,
                'game_state': game.get_game_state()
            }, room=game_id)
        else:
            emit('error', {'message': 'Color already taken'})
    else:
        emit('error', {'message': 'Game not found'})

@socketio.on('leave_game')
def on_leave_game(data):
    game_id = data['game_id']
    if game_id in games:
        leave_room(game_id)
        emit('player_left', {'sid': request.sid}, room=game_id)

if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0', port=5000) 