from tools import interface, benchmark


def main():
    QSB = interface.Interface()
    (
        platform,
        provider,
        backend,
        algorithm,
        benchmark,
        num_qubits,
        num_shots,
    ) = QSB.get_user_inputs()

    # [ ]: It will be completed.
    
if __name__ == "__main__":
    main()
