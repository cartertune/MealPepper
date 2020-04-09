import React from "react";

class Plan extends React.Component {
    constructor(props) {
        super(props);
        this.state = {};
    }

    render() {
        return (
            <div className="plan">
                {this.props.plan}
            </div>
        );
    }
};

export default Plan;