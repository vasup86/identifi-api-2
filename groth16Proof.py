import json
import subprocess


def verifyMDL(mdlData):
    
    # Convert JSON fields into integers
    issuer = int(mdlData["issuer"])
    id_number = int(mdlData["id_number"])
    date_of_birth = int(mdlData["date_of_birth"])
    signature = int(mdlData["signature"], 16)  # Convert hex to integer

    # Create a Circom input file
    input_data = {
        "issuer": issuer,
        "id_number": id_number,
        "date_of_birth": date_of_birth,
        "signature": signature
    }

    with open("input.json", "w") as f:
        json.dump(input_data, f)

    # Generate witness
    subprocess.run(["snarkjs", "witness", "calculate", 
                    "mdl_verifier.wasm", "input.json", "witness.wtns"
                    ])

    # Generate proof
    subprocess.run(["snarkjs", "groth16", "prove", "mdl_final.zkey",
                    "witness.wtns", "proof.json", "public.json"
                   ])


    #Verify the proof
    subprocess.run(["snarkjs", "groth16", "verify", 
                    "verification_key.json", "public.json", "proof.json"
                    ])

    # return the proof