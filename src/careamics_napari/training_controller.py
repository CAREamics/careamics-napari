
from careamics_napari.training_widget import TrainWidget

class TrainingController:

    def __init__(self) -> None:
        
        self.train_widget = TrainWidget()

    def get_widget(self) -> TrainWidget:
        return self.train_widget
    

if __name__ == "__main__":
    from qtpy.QtWidgets import QApplication
    import sys

    # Create a QApplication instance
    app = QApplication(sys.argv)

    # Instantiate widget
    controller = TrainingController()
    widget = controller.get_widget()

    # Show the widget
    widget.show()

    # Run the application event loop
    sys.exit(app.exec_())