import { Component } from '@angular/core';
import { WebsocketService } from './websocket.service';
import { Observer, Subject } from 'rxjs/Rx';
import * as io from 'socket.io-client';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  title = 'app';

}
