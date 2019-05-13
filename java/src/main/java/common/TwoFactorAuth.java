package common;

import com.google.common.primitives.UnsignedBytes;
import org.apache.commons.codec.binary.Base32;

import javax.crypto.Mac;
import javax.crypto.spec.SecretKeySpec;
import java.security.InvalidKeyException;
import java.security.NoSuchAlgorithmException;
import java.util.Arrays;
import java.util.Scanner;

/**
 * <b>Pseudocode for one-time password (OTP)</b>
 * <pre>
 * function GoogleAuthenticatorCode(string secret)
 *       key := 5B5E7MMX344QRHYO
 *       message := floor(current Unix time / 30)
 *       hash := HMAC-SHA1(key, message)
 *       offset := last nibble of hash
 *       truncatedHash := hash[offset..offset+3]  //4 bytes starting at the offset
 *       Set the first bit of truncatedHash to zero  //remove the most significant bit
 *       code := truncatedHash mod 1000000
 *       pad code with 0 from the left until length of code is 6
 *       return code
 * </pre>
 *
 * @see <a href="https://en.wikipedia.org/wiki/Google_Authenticator">Wiki</a>
 */
public class TwoFactorAuth {
    private static final String HMAC_SHA1 = "HmacSHA1";
    private static final short[] SHIFTS = {56, 48, 40, 32, 24, 16, 8, 0};

    private static byte[] toBytes(long value) {
        byte[] result = new byte[8];
        for (int i = 0; i < SHIFTS.length; i++) {
            result[i] = (byte) ((value >> SHIFTS[i]) & 0xFF);
        }
        return result;
    }

    private static int toUint32(byte[] bytes) {
        return (UnsignedBytes.toInt(bytes[0]) << 24)
                + (UnsignedBytes.toInt(bytes[1]) << 16)
                + (UnsignedBytes.toInt(bytes[2]) << 8)
                + (UnsignedBytes.toInt(bytes[3]));
    }

    private static int oneTimePassword(byte[] key, byte[] value) throws InvalidKeyException, NoSuchAlgorithmException {
        Mac mac = Mac.getInstance(HMAC_SHA1);
        mac.init(new SecretKeySpec(key, HMAC_SHA1));
        mac.update(value);
        byte[] hash = mac.doFinal();

        int offset = hash[hash.length - 1] & 0x0F;

        byte[] truncatedHash = Arrays.copyOfRange(hash, offset, offset + 4);

        truncatedHash[0] = (byte) (truncatedHash[0] & 0x7F);

        long number = toUint32(truncatedHash);

        return (int) (number % 1000000);
    }

    public static void main(String[] args) throws NoSuchAlgorithmException, InvalidKeyException {
        Scanner scanner = new Scanner(System.in);
        System.out.print("Input key:");
        String input = scanner.nextLine();
        scanner.close();

        byte[] key = new Base32().decode(input);
        long epochSeconds = System.currentTimeMillis() / 1000;
        int pwd = oneTimePassword(key, toBytes(epochSeconds / 30));
        long secondsRemaining = 30 - (epochSeconds % 30);

        System.out.println(String.format("%06d (%d second(s) remaining)", pwd, secondsRemaining));
    }
}

