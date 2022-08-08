import React, { Component } from "react";
import Card from "./Card";

interface HandOfCardsProps {
    cards:any[];
}

interface HandOfCardsState {
    conversion:Map<Number, string>;
}

class HandOfCards extends Component<HandOfCardsProps, HandOfCardsState> {
    constructor(props: HandOfCardsProps) {
        super(props);
        let map = new Map<Number, string>();
        map.set(0, "Land");
        map.set(1, "0 mana acceleration");
        map.set(2, "1 mana acceleration");
        map.set(3, "1 mana threat");
        map.set(4, "2 mana threat");
        map.set(5, "3 mana threat");
        map.set(6, "4 mana threat");
        map.set(7, "5 mana threat");
        map.set(8, "Interaction");

        this.state = {conversion: map};
    }
    
    render() {
        let cardObjects = [];
        let counter = 0;
        for (let i = 0; i < this.props.cards.length; i++) {
            for (let j = 0; j < this.props.cards[i]; j++) {
                cardObjects.push(<Card type={this.state.conversion.get(i)} key={counter}/>);
                counter++;
            }
        }
        return (
            <div>
                {cardObjects}
            </div>
        );
    }
}

export default HandOfCards;
