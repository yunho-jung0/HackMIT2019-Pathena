import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { InputHandleComponent } from './input-handle.component';

describe('InputHandleComponent', () => {
  let component: InputHandleComponent;
  let fixture: ComponentFixture<InputHandleComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ InputHandleComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(InputHandleComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
