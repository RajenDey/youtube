import React, { Component } from 'react';
import axios from 'axios';

export default class Main extends Component {
    state = {
        video: null,
    }

    render() {
        if (this.state.video === null) {
            return null;
        }
        return (
            <div className="main-page" style={{textAlign: 'center'}}>
                <h1 className="main-page-header">Youtube!</h1>
                <iframe src={`https://www.youtube.com/embed/${this.state.video.id}?&autoplay=1`}
                frameborder='0'
                allow='autoplay; encrypted-media'
                allowfullscreen
                title='video'
                height='800'
                width="1200px"
                />
                <p></p>
                <button onClick={this.handleClick}>Next Video!</button>
            </div>
        )
    }

    componentDidMount() {
        this.handleClick();
    }


    handleClick = () => {
        axios.get("http://localhost:5000")
        .then(res => {
            this.setState({
                video: res.data,
            });
        })
        .catch(err => {

        })
    }
}