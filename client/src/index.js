import React from "react";
import ReactDOM from "react-dom";
import './index.css';

class Board extends React.Component {
	constructor(props) {
		super(props);
		this.state = {
			squares: Array(9).fill(null),
		}
	}

	renderSquare(i) {
		return <Square value={this.state.squares[i]} />;
	}

	render() {
		return (
			<div>
				<div className="board-row">
					{this.renderSquare(1)}
					{this.renderSquare(2)}
					{this.renderSquare(3)}
				</div>
				<div className="board-row">
					{this.renderSquare(4)}
					{this.renderSquare(5)}
					{this.renderSquare(6)}
				</div>
				<div className="board-row">
					{this.renderSquare(7)}
					{this.renderSquare(8)}
					{this.renderSquare(9)}
				</div>
			</div>
		);
	}
}

class Square extends React.Component {
	constructor(props) {
		super(props);
		this.state = {
			value: null,
		}

	}

	render() {
		return (
			<button
				className="square"
				onClick={() => this.setState({ value: 'X' })}
			>
				{this.state.value}
			</button>
		);
	}	
}

function App() {
	return (
		<Board />
	);
}

const root = ReactDOM.createRoot(
	document.getElementById('root')
);

root.render(<App />);