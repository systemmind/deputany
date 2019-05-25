import React, { Component } from 'react';
import './App.css';
import { Link } from 'react-router-dom'


class ImportFile extends Component{
  constructor(props){
    super(props)
     this.state = {
       fileReader: new FileReader()
     }
     this.load_user_votes = this.load_user_votes.bind(this)
     this.handleFile = this.handleFile.bind(this)
  }

  handleFile (e){
    console.log("handleFile")
    const content = this.state.fileReader.result;
    console.log(content)
    this.props.call_back(content)
    
  }

  load_user_votes (file){
    console.log("load_user_votes")
    this.state.fileReader.onloadend = this.handleFile;
    this.state.fileReader.readAsText(file);
  }

  render(){
  return (<div style={{position: "fixed", left: 650, bottom: 500}}>
  <input type="file" id="file" accept=".txt" onChange={e => this.load_user_votes(e.target.files[0])}></input>
  </div>)
  }
}

function enactment (props){
  return(
      <div style={{textAlign: "left",
                   marginTop: "20px"}}>{props.description}
      </div>
  )
}

function show_candidates(candidates, len){
  if(candidates.length){
    const table=candidates.map(candidat => <tr key={candidat[0]}><td onClick ={() => window.open(candidat[0], '_blank')}>інформація</td>
                                                                 <td>{candidat[1]['name']}</td>
                                                                 <td align='center'>{candidat[1]['matches']+'/'+len}</td></tr>)
    return(
      <div style={{position: "fixed",
                   left:600, bottom:400}}>
      <table border = "1">
      <tbody>
      <tr><th>url</th><th>ФИО</th><th>совпадения голосов</th></tr>
      {table}
      </tbody>
      </table>
      </div>
    )
  }

}

class TopEnactments extends Component{
  constructor(props){
    super(props)
    this.state = {
      enactments: [],
      loading: true,
      index: 0,
      user_enactments: [],
      candidates: [],
      load_user_votes: false
    }

  this.index_up = this.index_up.bind(this)
  this.index_down = this.index_down.bind(this)
  this.check_vote = this.check_vote.bind(this)
  this.save_user_votes = this.save_user_votes.bind(this)
  this.send_on_server_get_result = this.send_on_server_get_result.bind(this)
  this.load_user_votes = this.save_user_votes.bind(this)
  this.call_back_get_data_from_file = this.call_back_get_data_from_file.bind(this)
  }

  index_up(){
    const {index, enactments} = this.state
    if(index < enactments.length-1){
      this.setState({index: this.state.index+1})
    }
  }

  index_down(){
    let index = this.state.index
    if(index > 0){
      this.setState({index: this.state.index-1})
    }
  }  

  check_vote(value){
    console.log(this.state.enactments[this.state.index])
    console.log(value)
    let user_enactments = this.state.user_enactments
    const url = this.state.enactments[this.state.index].url
    if(!user_enactments.find(elem => elem.enactment == url ))
      user_enactments.push(
        {
          "enactment": url,
          "vote": value
        }
      )
      this.setState({user_enactments: user_enactments })
      console.log(this.state.user_enactments)
  }


  
  save_user_votes(){
    var element = document.createElement('a');
    element.setAttribute('href', 'data:text/plain;charset=utf-8,' + encodeURIComponent(JSON.stringify(this.state.user_enactments)));
    element.setAttribute('download', 'my_votes');
    element.style.display = 'none';
    document.body.appendChild(element);
    element.click();
    document.body.removeChild(element);
  }

  send_on_server_get_result(){
    let dict = []
    fetch('http://127.0.0.1:5000/db_api/process', {
      method: 'POST',
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(this.state.user_enactments)
    })
    .then(response => response.json())
    .then(arr => this.setState({candidates: arr}))
    .catch(error => console.log(error))
  }

  call_back_get_data_from_file = (data) => {
    this.setState({user_enactments: JSON.parse(data), load_user_votes: false})
  }

  componentDidMount(){
    if(!this.state.candidates.length){
      this.setState({loading: true})
      fetch('http://127.0.0.1:5000/db_api/topenactments')
      .then(response => response.json())
      .then(json => json.enactments)
      .then(arr => this.setState({enactments: arr, loading: false}))
      .catch(error => console.log(error))
    }

  }

  render(){
    const {enactments, loading, index, candidates, user_enactments, load_user_votes} = this.state
    console.log(index);
    if(load_user_votes){
      return <ImportFile call_back={this.call_back_get_data_from_file}/>
    }
    if (loading){
      return <div>Loading enactments...</div>;
    }

    if (!enactments.length){
      return <div>No enactments</div>;
    }
    if(!candidates.length){
      return (
        <div>
          <center>
            <div style={{width: "60%"}}>
              <div style={{textAlign: "center"}}>
                <a href='#' onClick={this.save_user_votes}>Зберегти</a> | 
                <a href='#' onClick={this.send_on_server_get_result}>Кандидати</a> | 
                <a href='#' onClick={() => this.setState({load_user_votes: true})}>Завантажити</a>
                <a  href='#' style = {{fontFamily: "Consolas", float: "left", fontSize: "40pt", textDecoration: "none", marginTop: "40px"}} onClick={this.index_down}> {'<'} </a>
                <a href='#' style = {{fontFamily: "Consolas", float: "right", fontSize: "40pt", textDecoration: "none", marginTop: "40px"}} onClick={this.index_up}>{'>'} </a>
                <div style={{ width: "80%", left: "10%", position: "relative"}}>{enactment(enactments[index])}</div>
                <br></br>
                <br></br>
                <div name="voting">
                  <button  onClick={() => this.check_vote("За")} style={{border: "none", backgroundColor: "transparent", color: 'none', fontSize: "40pt", width: "200px"}}>	&#x1f44d;</button>
                  <button  onClick={() => this.check_vote("Проти")} style={{border: "none", backgroundColor: "transparent", color: 'none', fontSize: "40pt", width: "200px"}}>&#x1f44e; </button>
                </div>
              </div>
            </div>
          </center>
        </div>
      )
    }
    if(candidates.length){
      return (
        <div>{show_candidates(candidates, user_enactments.length)}
          <button style = {{position: "fixed", left: 740, bottom: 200}} onClick={() => this.setState({candidates:[]})}>Прожовжити голосування</button>
        </div>

      )
    }
  }
}

class App extends Component {
  constructor(props){
    super(props);
  }
    
    render() {
   
      return (
        <div>
          <TopEnactments></TopEnactments>
        </div>
        )
  }
}
export default App;
