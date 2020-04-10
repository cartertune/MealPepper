import React from "react";

class ConstraintForm extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            caloriesMin: "0",
            caloriesMax: "0",
            proteinMin: "0",
            proteinMax: "0",
            cholesterolMin: "0",
            cholesterolMax: "0",
            fiberMin: "0",
            fiberMax: "0",
            calciumMin: "0",
            calciumMax: "0",
            sugarMin: "0",
            sugarMax: "0",
            sodiumMin: "0",
            sodiumMax: "0",
            carbohydratesMin: "0",
            carbohydratesMax: "0",
            ironMin: "0",
            ironMax: "0",
            vitaminAMin: "0",
            vitaminAMax: "0",
            vitaminB12Min: "0",
            vitaminB12Max: "0",
            vitaminCMax: "0",
            vitaminCMin: "0",
            vitaminEMin: "0",
            vitaminEMax: "0",
            fatMin: "0",
            fatMax: "0",
            dietsSelected: [],
            loading: false
        };
    }

    textInputValueChange = (event, stateValueString) => {
        this.setState({[stateValueString]: event.target.value})
    };

    createConstraintInputJsx = (constraint) => {
        return (
            <input 
                className="constraint-input" 
                type="number" 
                value={this.state[constraint]} 
                onChange={(event) => {this.textInputValueChange(event, constraint)}} />
        );
    };

    createConstraintMinMaxInputJsx = (constraint, label = constraint) => {
        const constraintMinString = `${constraint}Min`;
        const constraintMaxString = `${constraint}Max`;

        return (
            <>
                <div><b>{label}:</b></div>
                <span>min:</span>
                {this.createConstraintInputJsx(constraintMinString)}
                <span>max:</span>
                {this.createConstraintInputJsx(constraintMaxString)}
            </>
        );
    };

    selectOptionsChange = (event) => {
        const dietsSelected = [];
        const { options } = event.target;
        for (let i = 0; i < options.length; i++) {
            if (options[i].selected) {
                dietsSelected.push(options[i].value);
            }
        }
        this.setState({dietsSelected});
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
        const { loading } = this.state;

        return (
            <div className="constraint-form">
                {this.createConstraintMinMaxInputJsx("calories")}
                {this.createConstraintMinMaxInputJsx("protein")}
                {this.createConstraintMinMaxInputJsx("cholesterol")}
                {this.createConstraintMinMaxInputJsx("fiber")}
                {this.createConstraintMinMaxInputJsx("calcium")}
                {this.createConstraintMinMaxInputJsx("sugar")}
                {this.createConstraintMinMaxInputJsx("sodium")}
                {this.createConstraintMinMaxInputJsx("carbohydrates")}
                {this.createConstraintMinMaxInputJsx("iron")}
                {this.createConstraintMinMaxInputJsx("vitaminA", "vitamin A")}
                {this.createConstraintMinMaxInputJsx("vitaminB12", "vitamin B12")}
                {this.createConstraintMinMaxInputJsx("vitaminC", "vitamin C")}
                {this.createConstraintMinMaxInputJsx("vitaminE", "vitamin E")}
                {this.createConstraintMinMaxInputJsx("fat")}

                <div className="diet-selector">
                    <div><b>diet</b></div>
                    <select onChange={this.selectOptionsChange} size="8" multiple>
                        <option value="dairy-free">dairy-free</option>
                        <option value="engine-2">engine 2</option>
                        <option value="gluten-free">gluten-free</option>
                        <option value="low-sodium">low sodium</option>
                        <option value="paleo-friendly">paleo</option>
                        <option value="vegan">vegan</option>
                        <option value="vegetarian">vegetarian</option>
                        <option value="keto-friendly">keto</option>
                    </select>
                </div>

                <div className="generate-plan-button">
                    <button disabled={loading} onClick={this.generatePlan}>
                        <b>generate plan</b>
                    </button>
                </div>
            </div>
        );
    }
};

export default ConstraintForm;