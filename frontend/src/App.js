import axios from 'axios';
import React from 'react';

class App extends React.Component {

    state = { details: [] };

    componentDidMount() {
        let data;
        axios.get('http://localhost:8000/api/react/')
        .then(res => {
            data = res.data;
            this.setState({ details: data });
        })
        .catch(err => {
            console.error(err);
        });
    }

    render() { 
        return (
            <div>
                <header>
                    Data Generated From Django
                </header>
                <hr />
                {this.state.details.map((output, id) => (
                    <div key={id}>
                        <h1>{output.employee}</h1>
                        <p>{output.department}</p>
                    </div>
                ))}
            </div>
        );
    }
}

export default App;
