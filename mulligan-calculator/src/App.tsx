import React, { Component } from "react";

// Allows us to write CSS styles inside App.css, any styles will apply to all components inside <App />
import "./App.css";
import HandOfCards from "./HandOfCards";

const NUM_CARD_TYPES = 9;
const NUM_CARS_IN_HAND = 7;


interface AppState {
    cards: any[];
}


class App extends Component<{}, AppState> {
    constructor(props: any) {
        super(props);
        this.state = {cards: this.compileCards()};
    }
    render() {
        return (
            <div className="center">
                <HandOfCards cards={this.state.cards}/>
                <div className="centerButton">
                    <button onClick={() => this.saveData(true)}>Keep</button>
                    <button onClick={() => this.saveData(false)}>Mulligan</button>
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

    saveData(isKept:boolean) {
        this.setState({cards: this.compileCards()});
    }


}

export default App;
