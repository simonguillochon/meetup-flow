import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ConferenceDialogComponent } from './conference-dialog.component';

describe('ConferenceDialogComponent', () => {
  let component: ConferenceDialogComponent;
  let fixture: ComponentFixture<ConferenceDialogComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ConferenceDialogComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(ConferenceDialogComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
