import React, { Component } from "react";

interface CardProps {
    type:string | undefined;
}

interface CardState {}

class Card extends Component<CardProps, CardState> {
    render() {
        return (
            <div className="rectangle"> {this.props.type}</div>
        );
    }
}

export default Card;
