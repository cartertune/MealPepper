import React from "react";
import ConstraintForm from "./ConstraintForm";
import Plan from "./Plan";

class MealPepperContainer extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            plan: ""
        };
    }

    setPlan = (plan) => {
        this.setState({plan});
    }

    render() {
        return (
            <div className="meal-pepper-container">
                <h1>Meal Pepper</h1>
                <ConstraintForm setPlan={this.setPlan} />
                <Plan plan={this.state.plan} />
            </div>
        );
    }
};

export default MealPepperContainer;