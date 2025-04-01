import { ComponentFixture, TestBed } from '@angular/core/testing';

import { WaitingIncidentsComponent } from './waiting-incidents.component';

describe('WaitingIncidentsComponent', () => {
  let component: WaitingIncidentsComponent;
  let fixture: ComponentFixture<WaitingIncidentsComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [WaitingIncidentsComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(WaitingIncidentsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
