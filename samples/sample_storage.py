import sys
import os, uuid
from dotenv import find_dotenv, load_dotenv

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from shared.blobstorage import BlobStorage

def main() -> None:    
    load_dotenv(find_dotenv())

    summary = """
        Tim Horton was a hockey player but is the name of a coffee chain, which means my dream of a goat sanctuary being my legacy is not unrealistic. If a dog and cat had a baby together that grew up and worked a desk job he'd be a Cog in the machine. This is a true fact: I never had a fear of heights until I fell off a roof. why does that make love so special?. For the name of an act as serious as killing someone, assassination literally translates to buttbuttination. A tagline for a special highway that is easy to navigate while under the influence of drugs: Take the High Road. A tagline for an airline: Take the High Road. You say potatoe, I say starchy carbs. Why don't we call glasses duocles. I bet most serial killers play the drums.", '["Refugee", "Vulnerable People", "Displaced"], ["USA", "United States", "United States of America", "US"]', 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nunc sagittis nisl quam, at eleifend odio ornare sit amet. Nullam efficitur, metus non sollicitudin pharetra, augue ante pulvinar erat, id aliquam lacus leo non arcu. Mauris aliquet, nulla ac iaculis ultricies, ligula ipsum ornare leo, at mattis ante elit et sapien. Sed vehicula, justo a dapibus finibus, justo neque hendrerit tellus, ut scelerisque leo nisi sit amet sem. Suspendisse congue sapien orci, sit amet congue nisl pulvinar eu. Nulla auctor nibh a turpis varius, a pharetra tellus laoreet. Sed at laoreet justo, vel cursus nisi.
    """
    filename = f'ukraine_{str(uuid.uuid4())}.txt'
    storage = BlobStorage()
    storage.upload(os.environ['Storage_JobContainerName'], filename, summary)

if __name__ == '__main__':
    main()