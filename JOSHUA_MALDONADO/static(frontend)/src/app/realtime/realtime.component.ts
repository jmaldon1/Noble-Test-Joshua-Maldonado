import { Component, OnInit } from '@angular/core';
import { WebsocketService } from '../websocket.service';
import { Observer, Subject } from 'rxjs/Rx';
import * as io from 'socket.io-client';

@Component({
  selector: 'app-realtime',
  templateUrl: './realtime.component.html',
  styleUrls: ['./realtime.component.css']
})
export class RealtimeComponent {

  dataArray: Array<{price:String, count:String, buy:String, sell:String}> = [];
  //this constructor will call the WebsocketService in websocket.service.ts
  constructor(private websocket:WebsocketService) {
  	this.websocket.orderBookData()
  	//must use subscribe because orderBookData() is returning an observable
  	//then it will push the data into the data array
  	.subscribe(data => this.dataArray.push(data));
  }

}
