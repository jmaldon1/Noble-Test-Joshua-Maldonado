import { Component, OnInit } from '@angular/core';
import { Http, Response, Headers } from '@angular/http';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';

@Component({
  selector: 'app-snapshot',
  templateUrl: './snapshot.component.html',
  styleUrls: ['./snapshot.component.css']
})
export class SnapshotComponent implements OnInit {
  rForm: FormGroup;
  GTprice:number;
  exchange:string = '';
  snapshotData:any;
  found:boolean=null;

  constructor(private fb: FormBuilder, private http:Http) { 
  	this.rForm = fb.group({
  		'GTprice': [null],
  		'exchange': 'All'
  	})
  }

  addPost(post){
  	this.GTprice = post.GTprice;
  	this.exchange = post.exchange;

  	// console.log(this.GTprice)
  	// console.log(this.exchange)
  	this.found = false;

  	//Various Get Requests to the REST api in flask server
  	if(this.exchange == 'All' && this.GTprice == null){
  		this.http.get('/snapshot')
  		.subscribe(
  			(data:any) => {
  				if(data.json()['snapshot_data'].length){
	  				this.snapshotData = data.json()
	  				this.found = true;
  				}
  			}
  		)
  	}
  	else if(this.GTprice != null && this.exchange == 'All'){
  		this.http.get(`/snapshotGreaterThan/${this.GTprice}`)
  		.subscribe(
  			(data:any) => {
  				if(data.json()['snapshot_data'].length){
	  				this.snapshotData = data.json()
	  				this.found = true;
	  			}
  			}
  		)
  	}
  	else if(this.exchange != 'All' && this.GTprice == null){
  		this.http.get(`/snapshotByExchange/${this.exchange}`)
  		.subscribe(
  			(data:any) => {
  				if(data.json()['snapshot_data'].length){
	  				this.snapshotData = data.json()
	  				this.found = true;
	  			}
  			}
  		)
  	}
  	else{
  		this.http.get(`/snapshotByExchangeAndPrice/${this.exchange}/${this.GTprice}`)
  		.subscribe(
  			(data:any) => {
  				if(data.json()['snapshot_data'].length){
	  				this.snapshotData = data.json()
	  				this.found = true;
	  			}
  			}
  		)
  	}

  }

  ngOnInit() {
  }

}
