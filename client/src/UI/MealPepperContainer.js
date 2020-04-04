import React from "react"

class MealPepperContainer extends React.Component {
    constructor(props) {
        super(props);
        this.state = {}
    }

    componentDidMount() {
        fetch('http://127.0.0.1:5000/')
            .then(res => res.json())
            .then((data) => {
                this.setState({text: data.data})
            }).catch(console.log)
      }

    render() {
        const { text } = this.state
        if (text) {
            return <div>{text}</div>
        }
        return <div>Loading...</div>
    }
}

export default MealPepperContainer