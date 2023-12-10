from tools import interface

def main():
    QSB = interface.Interface()
    print(QSB.get_user_inputs())
    # platform, provider, backend, algorithm, benchmark, num_qubits, num_shots = QSB.get_user_inputs()

if __name__ == "__main__":
    main()