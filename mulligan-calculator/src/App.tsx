import React, { Component } from "react";

// Allows us to write CSS styles inside App.css, any styles will apply to all components inside <App />
import "./App.css";
import HandOfCards from "./HandOfCards";

const NUM_CARD_TYPES = 9;
const NUM_CARS_IN_HAND = 7;


interface AppState {
    cards: any[];
    csv: any[];
}


class App extends Component<{}, AppState> {
    constructor(props: any) {
        super(props);
        this.state = {cards: this.compileCards(), csv: []};
    }
    render() {
        return (
            <div>
                <button onClick={() => this.saveData()}>Exit Session</button>
                <div className="center">
                    <HandOfCards cards={this.state.cards}/>
                    <div className="centerButton">
                        <button onClick={() => this.recordHand(true)}>Keep</button>
                        <button onClick={() => this.recordHand(false)}>Mulligan</button>
                    </div>
                </div>
            </div>
        );
    }

    // this method selects 7 random cards
    compileCards() {
        let toReturn = [];
        for (let i = 0; i < NUM_CARD_TYPES; i++) {
            toReturn.push(0);
        }
        for (let i = 0; i < NUM_CARS_IN_HAND; i++) {
            toReturn[Math.floor(Math.random() * NUM_CARD_TYPES)]++;
        }
        return toReturn;
    }

    // this method records if the current hand is kept or mulligan'ed
    // then appends the current hand to the data which we will eventually output
    recordHand(isKept:boolean) {
        if (isKept) {
            this.state.cards.push(1);
        } else {
            this.state.cards.push(0);
        }
        this.state.csv.push(this.state.cards)
        this.setState({cards: this.compileCards(), csv: this.state.csv});
    }


    saveData() {
        let csvContent = "data:text/csv;charset=utf-8,";

        this.state.csv.forEach(function(rowArray) {
            let row = rowArray.join(",");
            csvContent += row + "\r\n";
        });

        var encodedUri = encodeURI(csvContent);
        var link = document.createElement("a");
        link.setAttribute("href", encodedUri);
        link.setAttribute("download", "hands.csv");
        document.body.appendChild(link); // Required for FF

        link.click(); // This will download the data file named "hands.csv".
        this.setState({cards: this.compileCards(), csv: []})
    }
}

export default App;
