import pickle

from db_funcs import get_all_records, insert_record, get_column, \
    get_records_by_value, delete_all_records, get_first_record
from enc_funcs import BytesIntEncoder, generate_keypair, \
    encode_and_encrypt, decode_and_decrypt, calc_difference


def create_enc_obj(data, public_key):
    return encode_and_encrypt(BytesIntEncoder.encode(data.encode()), public_key)


def decrypt_obj(data, private_key):
    return BytesIntEncoder.decode(decode_and_decrypt(data, private_key)).decode()


def main():

    doc_table = 'documents'
    pers_table = 'person'

    frst_rec = get_first_record(pers_table)  #
    public_key = pickle.loads(frst_rec[5])   # !TMP KEYPAIR KEEPING!
    private_key = pickle.loads(frst_rec[4])  #

    while True:

        print("")
        print("'0' -> Update public and private keys (contained documents cannot be decrypted) [tmp]")
        print("'1' -> Show my encrypted docs [tmp]")
        print("'2' -> Create new doc")
        print("'3' -> Search doc by a title")
        print("'4' -> Delete all docs [tmp]")
        print("'5' -> Exit")
        print("")

        choice = int(input("Enter task number to perform it: "))
        print("")

        if choice == 0:

            delete_all_records(pers_table)                                              #
            public_key, private_key = generate_keypair()                                #
            record_to_insert = ('name', 'email', 'phone_number',                        # !JUST FOR TMP KEYPAIR KEEPING!
                                pickle.dumps(public_key), pickle.dumps(private_key))    #
            insert_record(pers_table, ('name', 'email', 'phone_number',                 #
                                       'public_key', 'passwd_hash'), record_to_insert)  #

            print("Public and private keys have been updated")

        elif choice == 1:

            records = get_all_records(doc_table)

            if len(records) != 0:
                for idx, row in enumerate(records):
                    print("")
                    print("#", idx + 1)
                    print("Title: ", pickle.loads(row[1]).ciphertext())
                    print("Content: ", pickle.loads(row[2]).ciphertext())
            else:
                print("No saved documents")

        elif choice == 2:

            title = str(input("Enter a title: "))
            enc_title = create_enc_obj(title, public_key)
            content = str(input("Enter a text: "))
            enc_content = create_enc_obj(content, public_key)

            record_to_insert = (pickle.dumps(enc_title), pickle.dumps(enc_content))
            insert_record(doc_table, ('title', 'content'), record_to_insert)

            print("New doc successfully added to storage")

        elif choice == 3:

            doc_was_found = False

            title = str(input("Enter a title: "))
            enc_title = create_enc_obj(title, public_key)

            records = get_column(doc_table, 'title')

            for idx, row in enumerate(records):
                diff = calc_difference(pickle.loads(row[0]), enc_title)
                if len(BytesIntEncoder.decode(decode_and_decrypt(diff, private_key))) == 0:
                    doc_was_found = True
                    documents = get_records_by_value(doc_table, 'title', row)

                    for document in documents:
                        enc_title = pickle.loads(document[1])
                        enc_content = pickle.loads(document[2])

                        print("")
                        print("#", idx + 1)
                        print("Title: ", decrypt_obj(enc_title, private_key))
                        print("Content: ", decrypt_obj(enc_content, private_key))

            if not doc_was_found:
                print("No documents with this title")

        elif choice == 4:

            delete_all_records(doc_table)
            print("All docs have been deleted")

        elif choice == 5:
            break

        else:
            print("Incorrect task")


if __name__ == "__main__":
    main()
