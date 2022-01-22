const scores = {
	player: 0,
	computer: 0
}

const choice_object = {
	'rock' : {
		'rock': 'draw',
		'paper': 'lose',
		'scissor': 'win'
	},
	'paper' : {
		'rock': 'win',
		'paper': 'draw',
		'scissor': 'lose'
	},
	'scissor' : {
		'rock': 'lose',
		'paper': 'win',
		'scissor': 'draw'
	}
}

const icons = {
	"rock": "far fa-hand-rock",
	"paper": "far fa-hand-paper",
	"scissor": "far fa-hand-scissors"
}

function computerSelect(){
	const choices = ["rock", "paper", "scissor"];
	let number = Math.floor(Math.random() * 3);
	return choices[number];
}

function updateScore(){
	const compScore = document.getElementById("comp_score");
	const playerScore = document.getElementById("player_score");
	
	playerScore.innerHTML = `Player Score : ${scores["player"]}`;
	compScore.innerHTML = `Computer Score : ${scores["computer"]}`;
}

function control(value){
	const resultBox = document.querySelector(".result-box");
	const resultText = document.querySelector(".result");
	
	switch(value){
		case "win": 
			resultBox.style.cssText = "background-color: #cefdce; color: #689f38";
			resultText.innerHTML = "WIN";
			scores["player"]++;
			break;
		case "lose":
			resultBox.style.cssText = "background-color: #ffdde0; color: #d32f2f";
			resultText.innerHTML = "LOSE";
			scores["computer"]++;
			break;
		case "draw":
			resultBox.style.cssText = "background-color: #e5e5e5; color: #808080";
			resultText.innerHTML = "DRAW";
			break;
	}
}

function updateIcon(choice){
	const compIcon = document.querySelector(".select i");
	compIcon.classList = icons[choice];
	if (compIcon.style.display == '') compIcon.style.display = "block";
}

function checkers(input){
	let computer_choice = computerSelect();
	
	//Seçimleri görüntülemek için konsola bak.
	console.log(`Player : ${input}`);
	console.log(`Computer : ${computer_choice}`);
	
	updateIcon(computer_choice);
	control(choice_object[input][computer_choice])
	updateScore();
}