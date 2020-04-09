import React from "react";

class ConstraintForm extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            caloriesMin: "0",
            caloriesMax: "0",
            loading: false
        };
    }

    caloriesMinChange = (event) => {
        this.setState({caloriesMin: event.target.value});
    };

    caloriesMaxChange = (event) => {
        this.setState({caloriesMax: event.target.value});
    };

    generatePlan = () => {
        this.setState({loading: true}, () => {
            fetch('http://127.0.0.1:5000/')
                .then(res => res.json())
                .then((data) => {
                    this.setState({loading: false});
                    this.props.setPlan(data.data);
                })
                .catch((error) => {
                    this.setState({loading: false});
                    console.error(error);
                });
        });    
    };

    render() {
        const {
            caloriesMin,
            caloriesMax,
            loading
        } = this.state;

        return (
            <div className="constraint-form">
                <div>calories:</div>
                <span>min:</span>
                <input className="constraint-input" type="number" value={caloriesMin} onChange={this.caloriesMinChange} />
                <span>min:</span>
                <input className="constraint-input" type="number" value={caloriesMax} onChange={this.caloriesMaxChange} />
                <div className="generate-plan-button">
                    <button disabled={loading} onClick={this.generatePlan}>
                        generate plan
                    </button>
                </div>
            </div>
        );
    }
};

export default ConstraintForm;