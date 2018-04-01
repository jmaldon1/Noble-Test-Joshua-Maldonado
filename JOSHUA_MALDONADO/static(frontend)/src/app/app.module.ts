import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { AppComponent } from './app.component';
import { BrowserAnimationsModule } from "@angular/platform-browser/animations";
import 'hammerjs';
import { RouterModule, Routes } from '@angular/router';
import { WebsocketService } from './websocket.service';
import { SnapshotComponent } from './snapshot/snapshot.component';
import { RealtimeComponent } from './realtime/realtime.component';
import { HttpModule } from '@angular/http';


const appRoutes: Routes = [
    {
        path: 'noble-markets-order-book-snapshot',
        component: SnapshotComponent
    },
    {
        path: 'noble-markets-realtime-order-book',
        component: RealtimeComponent
    },

];

@NgModule({
  declarations: [
    AppComponent,
    SnapshotComponent,
    RealtimeComponent
  ],
  imports: [
    RouterModule.forRoot(appRoutes),
    BrowserModule,
    BrowserAnimationsModule,
    HttpModule,
    ReactiveFormsModule
  ],
  providers: [
    WebsocketService
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }
