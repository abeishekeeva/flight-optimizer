import React from 'react';
import logo, { ReactComponent } from './logo.svg';
import './App.css';
import animation from './plane.gif';

class App extends React.Component {
  constructor(props) {
    super(props);
      this.state = {
        flightList: [],
        loading: false,
        message: null,
        departure_city: '',
        arrival_cities: ''
      }
      this.handleChange = this.handleChange.bind(this);
      this.handleSubmit = this.handleSubmit.bind(this);
  };


  handleChange = (e) => {
    this.setState({
        [e.target.className]: e.target.value
    })
  };
  
  handleSubmit = (e) => {
    e.preventDefault();
    
    let url = `http://127.0.0.1:8000/api/flights?departure=${encodeURIComponent(this.state.departure_city)}&arrival=${encodeURIComponent(this.state.arrival_cities)}`;
    this.setState({loading: true})
    fetch(url, {
      method: 'GET',
      headers: {
        'Accept': 'application/json'
      }
    })
    .then(response => response.json())
    .then(data => {
        
        this.setState({
          flightList: data["data"]
        })
        this.setState({
          message: data["error_message"]
        })
        this.setState({
          loading: false
        })
    })
    .catch(function(e){
        console.log("ERROR: ", e)
    })
};

  render() {
    var flights = this.state.flightList;
    var message = this.state.message;
    var flightsNotEmpty = (flights === undefined || flights == null || flights.length == 0) ? false : true;
    var loading = this.state.loading;
    
    return (
      <div className="wrapper">        
        <h1 id="header"> Flight Optimizer</h1>
        <div className="form-wrapper"> 
          <form id="form" onSubmit={this.handleSubmit}>
            <input onChange={this.handleChange} placeholder="Departure city" className="departure_city" type="text" required/>
            <input onChange={this.handleChange} placeholder="Arrival cities (separated by comma)" className="arrival_cities" type="text" required/>
            <button type="submit"> Search </button>
          </form>
        </div>

        <div className="list-wrapper">
          {loading ? <h3>Loading...</h3> : 
          <div id="table-div">
          {flightsNotEmpty ?
            <table>          
            <tr>
              <th>City</th>
              <th>Ratio ($/km)</th>
              <th>Distance (km)</th>
              <th>Price ($)</th>
            </tr>
              {flights.map(function(flight, index) {
                    return (
                        <tbody>
                        <tr>
                          <td>{flight[0]}</td>
                          <td>{flight[1]}</td>
                          <td>{flight[2]}</td>
                          <td>{flight[3]}</td>
                        </tr>
                        </tbody>
                                        
                    )
                })}
            </table> 
            :
            <h3 id="message">{message}</h3>
          }  
          </div>
          }
        
          <img src={animation}></img>
        </div>
      </div>

      
    );
  }
}


export default App;
