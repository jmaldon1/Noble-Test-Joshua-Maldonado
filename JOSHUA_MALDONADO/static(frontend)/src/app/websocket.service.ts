import { Injectable } from '@angular/core';
import * as io from 'socket.io-client';
import { Observable } from 'rxjs/Observable';
import * as Rx from 'rxjs/Rx';
import { environment } from '../environments/environment';

@Injectable()
export class WebsocketService {

	//Connect the client to the server
	private socket = io('localhost:5000');

	orderBookData(){
		let observable = new Observable<{price:String, count:String, buy:String, sell:String}>(observer => {
			//listening for 'my response' from server
			this.socket.on('my response', (data)=>{
				// console.log(data)
				//if data is recieved, it will pass the data along to realtime.component
				observer.next(data);
			});
			//if there is an error, disconnect the socket
			return () => {this.socket.disconnect();}
		});
		return observable;
	}

}
