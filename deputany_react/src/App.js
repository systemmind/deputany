import React, { Component } from 'react';
import './App.css';


class TopEnactments extends Component{
  constructor(props){
    super(props)
    this.state = {
      enactments: [],
      loading: false
    }
  }
  /*
  async _didMount(){
    try{
      this.setState({loading: true})
      const response = await fetch('http://127.0.0.1:5000/db_api/enactments');
      const json = await response.json();
      console.log(JSON.stringify(response));
      
      const descriptions = json.enactments.map(item => item.description);
      this.setState({enactments: descriptions, loading: false})
      console.log(this.state.enactments);
      console.log(this.state.loading)
      console.log(descriptions);
      
    }
    catch(err){
      console.error(err);
    }
  }
  */
  componentDidMount(){
    //this._didMount();
    this.setState({loading: true})
    let tmp =[]
    fetch('http://127.0.0.1:5000/db_api/enactments')
    .then(response => response.json())
    .then(json => json.enactments)
    
    //.then(arr => arr.map(elem => console.log(elem)))
    .then(arr => this.setState({enactments: arr, loading: false}))
    .catch(error => console.log(error));
    
    //console.log(this.state.enactments);
    //console.log(this.state.loading)
    //console.log(tmp) 
  }

  render(){
    //console.log(`render(): ${this.state.enactments}`);
    const {enactments, loading} = this.state
    console.log(`render(): ${enactments}`);
    if (loading){
      return <div>Loading enactments...</div>;
    }

    if (!enactments.length){
      return <div>No enactments</div>;
    }

    const list = enactments.map(item => <li>{item.description+"  "+   item.url}</li>);
    return (
      <ul>
        {list}
      </ul>
    );

    /*
    return (loading) ? <div>Loading enactments...</div>
                     : (!enactments.lenght)?
          <div>No enactments</div>:
            <ul>
              {enactments.map((enactment, url) => <li key={enactment}>url</li>)}
            </ul>
            */
  }
}

class App extends Component {
  constructor(props){
    super(props);
  }
    
    render() {
   
      return (
        <h2>Top enactments </h2>,
        <div>
          <TopEnactments></TopEnactments>
        </div>
        )
      
          
  }
}
export default App;
