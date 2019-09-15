import { Component, ElementRef,} from '@angular/core';
import { InputHandleComponent } from './input-handle/input-handle.component';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  constructor(private elementRef: ElementRef, private http2: HttpClient) {
  }
  title = '-- Street_Smart';

  ngAfterViewInit(){
    this.elementRef.nativeElement.ownerDocument.body.style.backgroundColor = 'Salmon'

  }
  
}
